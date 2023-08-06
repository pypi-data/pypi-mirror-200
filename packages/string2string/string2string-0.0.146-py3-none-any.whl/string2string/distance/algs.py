"""
    This module contains functions for computing different distance metrics between two strings.

    The algorithms implemented in this module include the following:
        (a) Levenshtein edit distance ++
        (b) Hamming edit distance ++
        (c) Damerau–Levenshtein edit distance ++ 
        (d) Jaccard distance ++ 
        (e) Jaccard similarity ++ 
        (f) Longest common substring ++ 
        (g) Longest common subsequence ++ 
"""

# Import relevant libraries and dependencies
from typing import List, Union, Tuple
import numpy as np


# Parent class for all the string algorithms implemented in this module
class StringAlgs:
    """
        This class is the parent class for all the string algorithms implemented in this module.
    """
    # Initialize the class
    def __init__(self,
                match_weight: float = 0.0,
        ) -> None:
        # Set the match weight
        self.match_weight = match_weight

    
    # Take the Cartesian product of two lists of strings (or lists of lists of strings)
    def cartesian_product(
        self,
        lst1: Union[List[str], List[List[str]]],
        lst2: Union[List[str], List[List[str]]],
        boolListOfList: bool = False,
    ) -> Union[List[str], List[List[str]]]:
        """
        This function returns the Cartesian product of two lists of strings (or lists of lists of strings).

        Arguments:
            lst1: The first list of strings (or lists of lists of strings).
            lst2: The second list of strings (or lists of lists of strings).
            boolListOfList: A boolean flag indicating whether the output should be a list of strings (or lists of lists of strings) (default: False).

        Returns:
            The Cartesian product of the two lists of strings (or lists of lists of strings).

        Examples:
            >>> from string2string.algs import StringAlgs
            >>> string_algs = StringAlgs()

            >>> string_algs.cartesian_product(["a", "b"], ["c", "d"])
            ['ac', 'ad', 'bc', 'bd']
            >>> string_algs.cartesian_product(["a", "b"], ["c", "d"], boolListOfList=True)
            ['a ## c', 'a ## d', 'b ## c', 'b ## d']
            >>> string_algs.cartesian_product(["abc"], ["xyz"], boolListOfList=True)
            ['abc ## xyz']
            >>> string_algs.cartesian_product(["abc"], ["xyz"], boolListOfList=False)
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


# Levenshtein edit distance class
class LevenshteinEditDistance(StringAlgs):
    def __init__(self,
                match_weight: float = 0.0,
                insert_weight: float = 1.0,
                delete_weight: float = 1.0,
                substitute_weight: float = 1.0,
    ) -> None:
        r"""
        This class initializes the Levenshtein edit distance algorithm. Levenshtein edit distance represents the minimum number of edit distance operations (insertion, deletion, and substitution) required to convert one string to another.
            
        The Levenshtein edit distance (with unit cost for each edit distance operation) is given by the following recurrence relation: 

        .. math::
            :nowrap:

            \begin{align}
            d[i, j] := \min( & d[i-1, j-1] + \texttt{mismatch}(i, j),  \\
                                & d[i-1, j] + 1,  \\
                                & d[i, j-1] + 1),
            \end{align}

        where :math:`\texttt{mismatch}(i, j)` is 1 if the i-th element in str1 is not equal to the j-th element in str2, and 0 otherwise.

        Arguments:
            match_weight (float): The weight of a match (default: 0.0).
            insert_weight (float): The weight of an insertion (default: 1.0).
            delete_weight (float): The weight of a deletion (default: 1.0).
            substitute_weight (float): The weight of a substitution (default: 1.0).

        Raises:
            AssertionError: If any of the weights are negative.
        """
        # Set the match weight
        super().__init__(match_weight=match_weight)

        # Set the insert, delete, and substite weights
        self.insert_weight = insert_weight
        self.delete_weight = delete_weight
        self.substitute_weight = substitute_weight

        # Assert that all the weights are non-negative
        assert min(match_weight, insert_weight, delete_weight, substitute_weight) >= 0.0


    # Compute the Levenshtein edit distance between two strings
    def compute(self,
        str1: Union[str, List[str]], 
        str2: Union[str, List[str]],
    ) -> float:
        r"""
        This function computes the Levenshtein edit distance between two strings (or lists of strings) using dynamic programming.

        Arguments:
            str1 (str or list of str): The first string (or list of strings).
            str2 (str or list of str): The second string (or list of strings).

        Returns:
            The Levenshtein edit distance between the two strings.

        .. note::
            * The solution presented here utilizes dynamic programming principles to compute the Levenshtein edit distance between two strings. 
            * This solution is also known as the Wagner-Fischer algorithm. [WF1974]_
            * The time complexity of this dynamic-programming-based solution is :math:`\mathcal{O}(nm)`, and the space complexity is :math:`\mathcal{O}(nm)`, where n and m are the lengths of the two strings, respectively.
            * However, by using only two rows of the distance matrix at a time, the space complexity of the dynamic programming solution can be reduced to :math:`\mathcal{O}(min(n, m))`.
            * The time complexity cannot be made strongly subquadratic time unless SETH is false. [BI2015]_
            * Finally, we note that this solution can be extended to cases where each edit distance operation has a non-unit cost.

            .. [WF1974] Wagner, R.A. and Fischer, M.J., 1974. The string-to-string correction problem. Journal of the ACM (JACM), 21(1), pp.168-173.
            .. [BI2015] Backurs, A. and Indyk, P., 2015, June. Edit distance cannot be computed in strongly subquadratic time (unless SETH is false). In Proceedings of the forty-seventh annual ACM symposium on Theory of computing (pp. 51-58).
        
        Examples:
            >>> from string2string.distance import LevenshteinEditDistance
            >>> levenshtein_edit_distance = LevenshteinEditDistance()

            >>> levenshtein_edit_distance.compute("kitten", "sitting")
            3.0
            >>> levenshtein_edit_distance.compute("aa", "bb")
            2.0
            >>> levenshtein_edit_distance.compute("aa", "aa")
            0.0
            >>> levenshtein_edit_distance.compute(["kurt", "godel"], ["godel", "kurt"])
            2.0
        """

        # Lengths of strings str1 and str2, respectively.
        n = len(str1)
        m = len(str2)

        # Initialize the distance matrix.
        dist = np.zeros((n + 1, m + 1))
        for i in range(1, n + 1):
            dist[i, 0] = self.delete_weight * i
        for j in range(1, m + 1):
            dist[0, j] = self.insert_weight * j

        # Dynamic programming step, where each operation has a unit cost:
        # d[i, j] := min(d[i-1, j-1] + mismatch(i, j), d[i-1, j] + 1, d[i, j-1] + 1),
        # where mismatch(i, j) is 1 if str1[i] != str2[j] and 0 otherwise.
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                # Compute the minimum edit distance between str1[:i] and str2[:j].
                dist[i, j] = min(
                    dist[i-1, j-1] + (self.substitute_weight if str1[i-1] != str2[j-1] else self.match_weight),
                    dist[i-1, j] + self.delete_weight, 
                    dist[i, j-1] + self.insert_weight,
                )

        # Return the Levenshtein edit distance between str1 and str2.
        return dist[n, m]


# Hamming (edit) distance class
class HammingDistance(StringAlgs):
    def __init__(self, 
                match_weight: float = 0.0,
                substitute_weight: float = 1.0,
        ) -> None:
        r"""
        This function initializes the class variables of the Hamming distance. 
        
        The Hamming distance is the number of positions at which the corresponding symbols are different. [H1950]_

        Arguments:
            match_weight (float): The weight of a match (default: 0.0).
            substitute_weight (float): The weight of a substitution (default: 1.0).

        Raises:
            AssertionError: If the substite weight is negative.

        .. note::
            * The Hamming distance has a time complexity of :math:`\mathcal{O}(n)`, where n is the length of the two strings.

        .. [H1950] Hamming, R.W., 1968. Error detecting and error correcting codes. Bell System Technical Journal, 29(2), pp.147-160.
        """
        # Set the match weight
        super().__init__(match_weight=match_weight)

        # Set the substite weight
        self.substitute_weight = substitute_weight

        # Assert that the substite weight is non-negative
        assert substitute_weight >= 0.0


    # Compute the Hamming distance between two strings
    def compute(self,
        str1: Union[str, List[str]], 
        str2: Union[str, List[str]],
    ) -> float:
        """
        This function computes the Hamming distance between two strings (or lists of strings).

        Arguments:
            str1 (str or list of str): The first string (or list of strings).
            str2 (str or list of str): The second string (or list of strings).

        Returns:
            The Hamming distance between the two strings.

        Raises:
            ValueError: If the two strings (or lists of strings) have different lengths.

        Examples:
            >>> from string2string.algs import HammingEditDistance
            >>> hamming_edit_distance = HammingEditDistance()

            >>> hamming_distance.compute("ab", "ba")
            2.0
            >>> hamming_distance.compute("Turing1912", "during1921")
            3.0
            >>> hamming_distance.compute("Earth", "earth")
            1.0
            >>> hamming_distance.compute(
                ["a", "ab", "abc", "abcd", "abc", "ab", "a"],
                ["a", "ab", "abc", "abcd", "abc", "ab", "a"],
                )
            0.0
        """

        # Lengths of strings str1 and str2, respectively.
        n = len(str1)
        m = len(str2)

        # Assert that the two strings have the same length
        if n != m:
            raise ValueError("The two strings (or lists of strings) must have the same length.")

        # Compute the Hamming edit distance between str1 and str2.
        return sum(
            self.substitute_weight if str1[i] != str2[i] else self.match_weight
            for i in range(n)
        )


# Damerau-Levenshtein edit distance class
class DamerauLevenshteinDistance(LevenshteinEditDistance):
    def __init__(self, 
                match_weight: float = 0.0,
                insert_weight: float = 1.0,
                delete_weight: float = 1.0,
                substitute_weight: float = 1.0,
                adjacent_transpose_weight: float = 1.0,
        ) -> None:
        r"""
        This function initializes the class variables of the Damerau-Levenshtein distance.
         
        The Damerau-Levenshtein edit distance is the minimum number of insertions, deletions, substitutions, and transpositions required to transform one string into the other. [D1964]_

        Arguments:
            match_weight (float): The weight of a match (default: 0.0).
            insert_weight (float): The weight of an insertion (default: 1.0).
            delete_weight (float): The weight of a deletion (default: 1.0).
            substitute_weight (float): The weight of a substitution (default: 1.0).
            adjacent_transpose_weight (float): The weight of an adjacent transposition (default: 1.0).

        Raises:
            AssertionError: If the insert, delete, substite, or adjacent transpose weights are negative.

        .. [D1964] Damerau, F.J., 1964. A technique for computer detection and correction of spelling errors. Communications of the ACM, 7(3), pp.171-176.
        """
        # Set the weights of the edit distance operations
        super().__init__(
            match_weight=match_weight,
            insert_weight=insert_weight,
            delete_weight=delete_weight,
            substitute_weight=substitute_weight,
        )

        # Set the adjacent transpose weight
        self.adjacent_transpose_weight = adjacent_transpose_weight

        # Assert that the adjacent transpose weight is non-negative
        assert adjacent_transpose_weight >= 0.0


    # Compute the Damerau-Levenshtein edit distance between two strings
    def compute(self,
        str1: Union[str, List[str]], 
        str2: Union[str, List[str]],
    ) -> float:
        """
        This function computes the Damerau-Levenshtein edit distance between two strings (or lists of strings).

        Arguments:
            str1 (str or list of str): The first string (or list of strings).
            str2 (str or list of str): The second string (or list of strings).

        Returns:
            The Damerau-Levenshtein distance between the two strings.

        .. note::
            * The Damerau-Levenshtein distance is a variant of the Levenshtein distance that allows for adjacent transpositions.
            * The dynamic programming solution to the Damerau-Levenshtein distance has a time complexity of :math:`\mathcal{O}(nm)`, where n and m are the lengths of the two strings.

        Examples:
            >>> from string2string.distance import DamerauLevenshteinEditDistance
            >>> damerau_levenshtein_edit_distance = DamerauLevenshteinEditDistance()

            >>> damerau_levenshtein_edit_distance.compute("ab", "ba")
            1.0
            >>> damerau_levenshtein_edit_distance.compute("wikiepdia", "wikipedia")
            1.0
            >>> damerau_levenshtein_edit_distance.compute("ababab", "bababa")
            2.0
            >>> damerau_levenshtein_edit_distance.compute(["kurt", "godel", "kurt"], ["godel", "kurt"])
            1.0
        """

        # Lengths of strings str1 and str2, respectively.
        n = len(str1)
        m = len(str2)

        # Initialize the distance matrix.
        dist = np.zeros((n + 1, m + 1))
        for i in range(1, n + 1):
            dist[i, 0] = self.delete_weight * i
        for j in range(1, m + 1):
            dist[0, j] = self.insert_weight * j

        # Dynamic programming solution to the Damerau-Levenshtein edit distance is very similar to that of the Levenshtein edit distance.
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                dist[i, j] = min(
                    dist[i-1, j-1] + (self.substitute_weight if str1[i-1] != str2[j-1] else self.match_weight),
                    dist[i-1, j] + self.delete_weight, 
                    dist[i, j-1] + self.insert_weight,
                )
                # This is the only difference between the Damerau-Levenshtein edit distance and the Levenshtein edit distance.
                if i > 1 and j > 1 and str1[i-1] == str2[j-2] and str1[i-2] == str2[j-1]:
                    dist[i, j] = min(dist[i, j], dist[i-2, j-2] + self.adjacent_transpose_weight)

        # Return the Damerau-Levenshtein edit distance between str1 and str2.
        return dist[n, m]


# Jacard index class
class JacardIndex:
    def __init__(self) -> None:
        r"""
        This function initializes the class variables of the Jacard index. 
        
        The Jacard index is equal to 1.0 minus the Jacard similarity coefficient. It is equal to 0.0 if and only if the two sets are equal. [J1938]_

        .. [J1938] Jaccard, P., 1912. The Distribution of the Flora in the Alpine Zone. New Phytologist, 11(2), pp.37-50.
        """
        pass

    # Compute the Jacard index between two strings
    def compute(self,
        str1: Union[str, List[str]], 
        str2: Union[str, List[str]],
    ) -> float:
        """
        This function computes the Jaccard index between two strings (or lists of strings).

        Arguments:
            str1 (str or list of str): The first string (or list of strings).
            str2 (str or list of str): The second string (or list of strings).

        Returns:
            The Jaccard index between the two strings.

        
        Examples:
            >>> from string2string.distance.algs import JacardIndex
            >>> jacard_index = JacardIndex()

            >>> jacard_index.compute("ab", "ba")
            0.0
            >>> jacard_index.compute("ab", "baaaaab")
            0.0
            >>> jacard_index.compute("ab", "bbbbaaaacd")
            0.5
            >>> jacard_index.compute("ab", "cd")
            1.0
        """

        # Lengths of strings str1 and str2, respectively.
        n = len(str1)
        m = len(str2)

        # Compute the Jacard index between str1 and str2.
        # The Jacard index is, by definition, equal to 1.0 minus the Jacard similarity coefficient.
        return 1. - len(set(str1).intersection(set(str2))) / len(set(str1).union(set(str2)))