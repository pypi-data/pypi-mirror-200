"""
    This module contains functions for computing different distance metrics between two strings.

    The algorithms implemented in this module include the following:
        (a) Levenshtein edit distance:
        (b) Hamming edit distance
        (c) Damerau–Levenshtein edit distance
        (d) Jaccard distance
        (e) Jaccard similarity
        (f) Longest common substring
        (g) Longest common subsequence
"""

# Import relevant libraries and dependencies
from typing import List, Union, Tuple
import numpy as np
from itertools import product


class EditDistAlgs:
    """
    This class contains functions for computing different distance metrics between two strings.
    """
    # Initialize the class
    def __init__(
        self,
        insert_weight: int = 1.0,
        delete_weight: int = 1.0,
        match_weight: int = 0.0,
        substite_weight: int = 1.0,
        adjacent_transposition_weight: int = 1.0,
        list_of_list_separator: str = " ## ",
    ) -> None:
        # All the weights should be non-negative.
        assert min(insert_weight, delete_weight, match_weight, substite_weight) >= 0

        # The weights for the different edit distance operations.
        self.insert_weight = insert_weight
        self.delete_weight = delete_weight
        self.match_weight = match_weight
        self.substite_weight = substite_weight
        self.adjacent_transposition_weight = adjacent_transposition_weight
        self.list_of_list_separator = list_of_list_separator


    # Cartesian product of two lists of strings (or lists of lists of strings)
    def stringlist_cartesian_product(
        self,
        lst1: Union[List[str], List[List[str]]],
        lst2: Union[List[str], List[List[str]]],
        boolListOfList: bool = False,
    ) -> Union[List[str], List[List[str]]]:
        """
        Definition:
            This function returns the Cartesian product of two lists of strings (or lists of lists of strings).

        Arguments:
            lst1: The first list of strings (or lists of lists of strings).
            lst2: The second list of strings (or lists of lists of strings).
            boolListOfList: A boolean flag indicating whether the output should be a list of strings (or lists of lists of strings) (default: False).

        Returns:
            The Cartesian product of the two lists of strings (or lists of lists of strings).

        Examples:
            >>> stringlist_cartesian_product(["a", "b"], ["c", "d"])
            ['ac', 'ad', 'bc', 'bd']
            >>> stringlist_cartesian_product(["a", "b"], ["c", "d"], boolListOfList=True)
            ['a ## c', 'a ## d', 'b ## c', 'b ## d']
            >>> stringlist_cartesian_product(["abc"], ["xyz"], boolListOfList=True)
            ['abc ## xyz']
            >>> stringlist_cartesian_product(["abc"], ["xyz"], boolListOfList=False)
            ['abcxyz']
        """
        if lst1 == []:
            return lst2
        elif lst2 == []:
            return lst1
        return [
            s1 + ("" if not (boolListOfList) else self.list_of_list_separator) + s2
            for s1 in lst1
            for s2 in lst2
        ]


    # Levenshtein edit distance
    def levenshtein_edit_distance(
        self, 
        str1: Union[str, List[str]], 
        str2: Union[str, List[str]],
    ) -> float:
        """
        Definition:
            This function computes the Levenshtein edit distance between two strings (or stringlists) using dynamic programming.

        Arguments:
            str1: The first string (or stringlist).
            str2: The second string (or stringlist).

        Returns:
            The Levenshtein edit distance between the two strings.

        Notes:
            (a) Levenshtein edit distance refers to the minimum number of edit distance oeprations (insertion, deletion, and substitution) needed to transform one string into another.
            (b) The simple dynamic programming solution, which penalizes each edit distance operation with a unit cost, is given by the following recurrence relation:
                d[i, j] := min(d[i-1, j-1] + mismatch(i, j), d[i-1, j] + 1, d[i, j-1] + 1),
                where mismatch(i, j) is 1 if str1[i] != str2[j] and 0 otherwise.
            (c) This solution is also known as the Wagner-Fischer algorithm (see: Wagner, R.A. and Fischer, M.J., 1974. The string-to-string correction problem. Journal of the ACM (JACM), 21(1), pp.168-173.)
            (d) The dynamic programming solution has a time complexity of O(nm) and a space complexity of O(nm), where n and m are the lengths of the two strings, respectively.
            (e) One can, however, easily improve the space complexity of the dynamic programming solution to O(min(n, m)) by using only two rows of the distance matrix at a time.
            (f) The time complexity, however, cannot be made strongly subquadratic time unless SETH is false.
                - See: "Edit Distance Cannot Be Computed in Strongly Subquadratic Time (unless SETH is false)" by Arturs Backurs (MIT) and Piotr Indyk (MIT), 2017. (Link: https://arxiv.org/pdf/1412.0348.pdf)
            (h) The Wagner-Fischer algorithm can be easily extended to the case where each edit distance operation has a non-unit cost.

        Examples:
            >>> levenshtein_edit_distance("kitten", "sitting")
            3.0
            >>> levenshtein_edit_distance("aa", "bb")
            2.0
            >>> levenshtein_edit_distance("aa", "aa")
            0.0
            >>> levenshtein_edit_distance(["kurt", "godel"], ["godel", "kurt"])
            2.0
        """

        # Lengths of strings str1 and str2, respectively.
        n = len(str1)
        m = len(str2)

        # Initialize the distance matrix of size (n+1) x (m+1)
        dist = np.zeros((n + 1, m + 1))
        for i in range(1, n + 1):
            dist[i, 0] = self.delete_weight * i
        for j in range(1, m + 1):
            dist[0, j] = self.insert_weight * j

        # Dynamic programming step (for the unit case where each operation has a unit cost):
        # d[i, j] := min(d[i-1, j-1] + mismatch(i, j), d[i-1, j] + 1, d[i, j-1] + 1),
        # where mismatch(i, j) is 1 if str1[i] != str2[j] and 0 otherwise.
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                dist[i, j] = min(
                    dist[i - 1, j - 1]
                    + (
                        self.substite_weight
                        if str1[i - 1] != str2[j - 1]
                        else self.match_weight
                    ),
                    dist[i, j - 1] + self.insert_weight,
                    dist[i - 1, j] + self.delete_weight,
                )
        return dist[n, m]


    # Damerau–Levenshtein edit distance
    def damerau_levenshtein_edit_distance(
        self, 
        str1: Union[str, List[str]], 
        str2: Union[str, List[str]],
    ) -> float:
        """
        Definition:
            This function computes the Damerau–Levenshtein edit distance between two strings (or stringlists) using dynamic programming.

        Arguments:
            str1: The first string (or stringlist).
            str2: The second string (or stringlist).

        Returns:
            The Damerau–Levenshtein edit distance between the two strings.

        Notes:
            (a) The Damerau–Levenshtein edit distance is an extension of the Levenshtein edit distance: It is defined as the minimum number of insertion, deletion, substitution, and adjacent transposition operations needed to transform one string into another.
            - In other words, Damerau–Levenshtein operations := Levenshtein edit distance operations + adjacent transposition.
            (b) The dyqnamic programming solution to this problem uses a simple extension of the Wagner-Fisher algorithm. It thus admits a quadratic space and time complexity.

        Examples:
            >>> damerau_levenshtein_edit_distance("ab", "ba")
            1.0
            >>> damerau_levenshtein_edit_distance("wikiepdia", "wikipedia")
            1.0
            >>> damerau_levenshtein_edit_distance("ababab", "bababa")
            2.0
            >>> damerau_levenshtein_edit_distance(["kurt", "godel", "kurt"], ["godel", "kurt"])
            1.0
        """

        # Lengths of strings str1 and str2, respectively.
        n = len(str1)
        m = len(str2)

        # Initialize the distance matrix of size (n+1) x (m+1)
        dist = np.zeros((n + 1, m + 1))
        for i in range(1, n + 1):
            dist[i, 0] = self.delete_weight * i
        for j in range(1, m + 1):
            dist[0, j] = self.insert_weight * j

        # Dynamic programming solution (similar to the Wagner-Fischer algorithm)
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                dist[i, j] = min(
                    dist[i - 1, j - 1]
                    + (
                        self.substite_weight
                        if str1[i - 1] != str2[j - 1]
                        else self.match_weight
                    ),
                    dist[i, j - 1] + self.insert_weight,
                    dist[i - 1, j] + self.delete_weight,
                )
                if (
                    i > 1
                    and j > 1
                    and str1[i - 1] == str2[j - 2]
                    and str1[i - 2] == str2[j - 1]
                ):
                    dist[i, j] = min(
                        dist[i, j],
                        dist[i - 2, j - 2] + self.adjacent_transposition_weight,
                    )

        return dist[n, m]


    # Hamming distance
    def hamming_distance(
        self, 
        str1: Union[str, List[str]],
        str2: Union[str, List[str]],
    ) -> float:
        """
        Definition:
            This function computes the Hamming distance between two strings (or list of strings) of equal length.

        Arguments:
            str1: The first string (or list of strings).
            str2: The second string (or list of strings).

        Returns:
            The Hamming distance between the two strings.

        Notes:
            (a) The Hamming distance is a metric for comparing two strings (or lists of strings) of equal length. It is equal to the number of positions at which the corresponding symbols are different.
        
        Examples:
            >>> hamming_distance("ab", "ba")
            2.0
            >>> hamming_distance("Turing1912", "during1921")
            3.0
            >>> hamming_distance("Earth", "earth")
            1.0
            >>> hamming_distance(
                ["a", "ab", "abc", "abcd", "abc", "ab", "a"],
                ["a", "ab", "abc", "abcd", "abc", "ab", "a"],
                )
            0.0
        """
        if len(str1) != len(str2):
            raise ValueError(
                "The lengths of the two strings (or lists of strings) must be equal."
            )

        dist = 0.0
        for i in range(len(str1)):
            # This is a more abstract implementation of the Hamming distance function.
            # In theory, it is possible for a match to have a cost as well.
            # For instance, we might want to penalize longer strings.
            dist += self.match_weight if str1[i] == str2[i] else self.substite_weight
        return dist


    # Jaccard similarity coefficient
    def jaccard_similarity_coefficient(
        self, 
        str1: Union[str, List[str]], 
        str2: Union[str, List[str]],
    ) -> float:
        """
        Definition:
            This function computes the Jaccard similarity coefficient between two strings (or lists of strings).

        Arguments:
            str1: The first string (or list of strings).
            str2: The second string (or list of strings).

        Returns:
            The Jaccard similarity coefficient between the two strings.

        Notes:
            (a) The Jaccard similarity coefficient measures the similarity between two "sets" of strings (or sets of lists of strings). It is equal to the ratio of the intersection over the union of the two sets.
            (b) The Jaccard similarity coefficient is equal to 1.0 if and only if the two sets are equal.

        Examples:
            >>> jaccard_similarity_coefficient("ab", "ba")
            1.0
            >>> jaccard_similarity_coefficient("ab", "baaaaab")
            1.0
            >>> jaccard_similarity_coefficient("ab", "bbbbaaaacd")
            0.5
            >>> jaccard_similarity_coefficient("ab", "cd")
            0.0
        """
        set1 = set(str1)
        set2 = set(str2)
        # Justification: In case both of them are empty strings.
        if str1 == str2:
            return 1.0
        return (len(set1.intersection(set2))) / (float(len(set1.union(set2))))

    
    # Jaccard index
    def jaccard_index(
        self, 
        str1: Union[str, List[str]], 
        str2: Union[str, List[str]]
    ) -> float:
        """
        Definition:
            This function computes the Jaccard index between two strings (or lists of strings).

        Arguments:
            str1: The first string (or list of strings).
            str2: The second string (or list of strings).

        Returns:
            The Jaccard index between the two strings.

        Notes:
            (a) The Jaccard index measures the dissimilarity between two "sets" of strings (or sets of lists of strings). It is equal to 1.0 minus the Jaccard similarity coefficient.
            (b) The Jaccard index is equal to 0.0 if and only if the two sets are equal.

        Examples:
            >>> jaccard_index("ab", "ba")
            0.0
            >>> jaccard_index("ab", "baaaaab")
            0.0
        """
        return 1.0 - self.jaccard_similarity_coefficient(str1, str2)

   
    # Longest common subsequence (LCSubseq)
    def longest_common_subsequence(
        self,
        str1: Union[str, List[str]],
        str2: Union[str, List[str]],
        printBacktrack: bool = False,
        boolListOfList: bool = False,
    ) -> Tuple[float, Union[List[str], List[List[str]]]]:
        """
        Definition:
            This function computes the longest common subsequence between two strings (or lists of strings).

        Arguments:
            str1: The first string (or list of strings).
            str2: The second string (or list of strings).
            printBacktrack: A boolean flag indicating whether to print the backtrack matrix.
            boolListOfList: A boolean flag indicating whether to return the longest common subsequence as a list of lists.

        Returns:
            The longest common subsequence between the two strings.

        Notes:
            (a) The longest common subsequence (which we denote by LCSubseq) of two strings is a subsequence of maximal length that appears in both of them.
            (b) The following dynamic programming solution has a quadratic (i.e., O(nm)) space and time complexity.
            (c) If the vocabulary is fixed, LCSubseq admits a "Four-Russians speedup," thereby reducing its overall time complexity to subquadratic (O(n^2/log n)).
            (d) The dynamic programming solution is based on the following recurrence:
                LCSubseq(str1, str2, i, j) = 
                {
                    if str1[i] == str2[j] then LCSubseq(str1, str2, i-1, j-1) + 1
                    else max(LCSubseq(str1, str2, i-1, j), LCSubseq(str1, str2, i, j-1))
                }
            (e) As in the case of the edit distance, the dynamic programming solution can be optimized further by using the last row of the matrix d to compute the longest common subsequence.

        Examples:
            >>> longest_common_subsequence("aa", "aa", printBacktrack=True)
            (2.0, ['aa'])
            >>> longest_common_subsequence("abcd", "xcxaaabydy", printBacktrack=True)
            (3.0, ['abd'])
            >>> longest_common_subsequence("aabbccdd", "dcdcbaba", printBacktrack=True)
            (2.0, ['dd', 'bb', 'cc', 'cd', 'aa', 'ab'])
            >>> longest_common_subsequence(["a", "bb", "c"],["a", "bb", "c"],printBacktrack=True,boolListOfList=True)
            3.0, [['a', 'bb', 'c']])
        """
        # Lengths of strings str1 and str2, respectively.
        n = len(str1)
        m = len(str2)

        # Initialize the matrix d of size (n+1) x (m+1)
        d = np.zeros((n + 1, m + 1))

        # Normally need to initialize d[i, j] = 0 for i =0 or j = 0
        # But that is already taken care of under this implementation since we initialize the matrix with all 0's.

        for i in range(1, n + 1):
            for j in range(1, m + 1):
                if str1[i - 1] == str2[j - 1]:
                    d[i, j] = d[i - 1, j - 1] + 1
                else:
                    d[i, j] = max(d[i - 1, j], d[i, j - 1])

        def backtrack(i: int, j: int) -> Union[List[str], List[List[str]]]:
            """
            Given the matrix d, backtracks and prints the set of "all" the longest subsequences.
            """
            if i == 0 or j == 0:
                return [""] if not (boolListOfList) else []
            if str1[i - 1] == str2[j - 1]:
                insert_elt = str1[i - 1] if not (boolListOfList) else [str1[i - 1]]
                final = list(
                    set(
                        self.stringlist_cartesian_product(
                            backtrack(i - 1, j - 1),
                            insert_elt,
                            boolListOfList=boolListOfList,
                        )
                    )
                )
                return final

            rest = []
            if d[i, j - 1] >= d[i - 1, j]:
                rest = backtrack(i, j - 1)
            if d[i - 1, j] >= d[i, j - 1]:
                rest += backtrack(i - 1, j)
            return list(set(rest))

        candidates = None
        if printBacktrack:
            candidates = backtrack(n, m)
            if boolListOfList and candidates:
                candidates = [
                    elt.split(self.list_of_list_separator) for elt in candidates
                ]
        return d[n, m], candidates

    
    # Longest common substring (LCSubstring)
    def longest_common_substring(
        self,
        str1: Union[str, List[str]],
        str2: Union[str, List[str]],
        printBacktrack: bool = False,
        boolListOfList: bool = False,
    ) -> Tuple[float, Union[List[str], List[List[str]]]]:
        """
        Definition:
            This function computes the longest common substring between two strings (or lists of strings).

        Arguments:
            str1: The first string (or list of strings).
            str2: The second string (or list of strings).
            printBacktrack: A boolean flag indicating whether to print the backtrack matrix.
            boolListOfList: A boolean flag indicating whether to return the longest common substring as a list of lists.

        Returns:
            The longest common substring between the two strings.

        Notes:
            (a) The longest common substring (which we denote by LCSubstring) of two strings is a substring of maximal length that appears in both of them.
            (b) The following dynamic programming solution has a quadratic (i.e., O(nm)) space and time complexity.
            (c) The dynamic programming solution is based on the following recurrence:
                LCSubstring(str1, str2, i, j) =
                {
                    if str1[i] == str2[j] then LCSubstring(str1, str2, i-1, j-1) + 1
                    else 0
                }
            (d) There is also a linear time solution based on generalized suffix trees.
            (e) As in the case of the edit distance, the dynamic programming solution can be optimized further by using the last row of the matrix d to compute the longest common substring.
            (f) Longest common substring is not the same as longest common subsequence.
            (g) The longest common substring is not necessarily unique.
            (h) The longest common substring is strictly contiguous.
            (i) The longest common substring is sometimes used to measure the similarity of two strings. It is also used in the field of computational biology to measure the similarity of two DNA sequences.
            (j) The longest common substring is also used in plagiarism detection, where it is used to measure the similarity of two texts.

        Examples:
            >>> longest_common_substring("aa", "aa", printBacktrack=True)
            (2.0, ['aa'])
            >>> longest_common_substring("xyxy", "yxyx", printBacktrack=True)
            (3, ['yxy', 'xyx'])
            >>> longest_common_substring("aabbaa", "aa", printBacktrack=True)
            (2, ['aa'])
            >>> longest_common_substring(" julia ", "  julie ", printBacktrack=True)
            (5, [' juli'])
        """
        # Lengths of strings str1 and str2, respectively.
        n = len(str1)
        m = len(str2)

        # Initialize the matrix d of size (n+1) x (m+1)
        # Here d[i,j] denotes the length of the longest common suffixes of substrings str1[:i] and str2[:j].
        d = np.zeros((n + 1, m + 1)).astype(int)

        max_length = 0
        max_length_indices = []
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                if str1[i - 1] == str2[j - 1]:
                    d[i, j] = d[i - 1, j - 1] + 1
                    if max_length < d[i, j]:
                        max_length = d[i, j]
                        max_length_indices = [i]
                    elif max_length == d[i, j]:
                        max_length_indices.append(i)
                else:
                    d[i, j] = 0
        candidates = None
        if printBacktrack:
            candidates = [str1[(i - max_length) : i] for i in max_length_indices]
            if boolListOfList:
                candidates = list(
                    set(
                        [
                            f"{self.list_of_list_separator}".join(cand)
                            for cand in candidates
                        ]
                    )
                )
                candidates = [
                    cand.split(self.list_of_list_separator) for cand in candidates
                ]
            else:
                candidates = list(set(candidates))
        return max_length, candidates