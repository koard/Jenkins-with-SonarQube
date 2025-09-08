from typing import List
def calculate_average(numbers: List[float]) -> float:
    """
    คำนวณค่าเฉลี่ยจาก list ของตัวเลข
    """
    if not numbers:
        raise ValueError("Numbers list must not be empty")
    return sum(numbers) / len(numbers)


def reverse_string(text: str) -> str:
    """
    กลับลำดับข้อความ
    """
    return text[::-1]

def unused_function():
    print("This function is never used")  # Code smell: unused function

def badName(x):
    y = 10  # Code smell: unused variable
    # TODO: Refactor this function
    return x
