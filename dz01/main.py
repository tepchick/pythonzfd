# TODO Given a sorted numsay of distinct integers and a target value, return the index if the target is found. If not, return the index where it would be if it were inserted in order.
def searchInsert(nums: list[int], target: int) -> int:
    if target in nums:
        return sorted(nums).index(target)
    else:
        nums.append(target)
        return sorted(nums).index(target)


# TODO Given a string s consisting of words and spaces, return the length of the last word in the string.
def lengthOfLastWord(s: str) -> int:
    s = s.split()
    return len(s[len(s) - 1])


# TODO Given an integer, convert it to a roman numeral.
def intToRoman(num: int) -> str:
    values = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    symbols = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
    result = ""
    for i, value in enumerate(values):
        while num >= value:
            num -= value
            result += symbols[i]
    return result


# TODO Given an array nums with n objects colored red, white, or blue, sort them in-place so that objects of the same color are adjacent, with the colors in the order red, white, and blue.
def sortColors(nums: list[int]) -> None:
    for i in range(len(nums)):
        for j in range(0, len(nums) - i - 1):
            if nums[j] > nums[j + 1]:
                nums[j], nums[j + 1] = nums[j + 1], nums[j]


# TODO Given an input string s, reverse the order of the words.
def reverseWords(s: str) -> str:
    return " ".join(reversed(s.split()))


# TODO Given a string containing digits from 2-9 inclusive, return all possible letter combinations that the number could represent.
from itertools import product


def letterCombinations(digits: str) -> list[str]:
    temp = {
        "2": "abc",
        "3": "def",
        "4": "ghi",
        "5": "jkl",
        "6": "mno",
        "7": "pqrs",
        "8": "tuv",
        "9": "wxyz",
    }
    comb = list(product(*[temp[x] for x in digits]))
    return ["".join(x) for x in comb] if len(comb) != 1 else []
