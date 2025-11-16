def print_relation(matrix, a):
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] == 1:
                print(f"({a[i]}, {a[j]})", end="")


def is_reflexive(matrix):
    for i in range(len(matrix)):
        if matrix[i][i] != 1:
            return False
    return True


def transpose_matrix(m):
    return [[m[j][i] for j in range(len(m))] for i in range(len(m[0]))]


def is_symmetric(m):
    return m == transpose_matrix(m)


def matrix_mult(a, b):
    size = len(a)
    result = [[0] * size for _ in range(size)]
    for i in range(size):
        for j in range(size):
            for k in range(size):
                result[i][j] |= a[i][k] & b[k][j]
    return result


def is_transitive(matrix):
    size = len(matrix)
    power = [row[:] for row in matrix]
    combined = [row[:] for row in matrix]

    for _ in range(1, size):
        power = matrix_mult(power, matrix)
        for i in range(size):
            for j in range(size):
                combined[i][j] |= power[i][j]
    return combined == matrix


def count_added_pairs(original_matrix, closure_matrix):
    size = len(original_matrix)
    count = 0
    for i in range(size):
        for j in range(size):
            if original_matrix[i][j] == 0 and closure_matrix[i][j] == 1:
                count += 1
    return count


def reflexive_closure(matrix):
    original_matrix = [row[:] for row in matrix]
    size = len(matrix)
    closure_matrix = [row[:] for row in matrix]
    for i in range(size):
        closure_matrix[i][i] = 1

    added_count = count_added_pairs(original_matrix, closure_matrix)
    print(f"반사 폐포를 위해 총 {added_count}개의 순서쌍이 추가되었습니다.")
    return closure_matrix


def symmetric_closure(matrix):
    original_matrix = [row[:] for row in matrix]
    size = len(matrix)
    transposed = transpose_matrix(matrix)
    closure_matrix = [row[:] for row in matrix]
    for i in range(size):
        for j in range(size):
            closure_matrix[i][j] = matrix[i][j] | transposed[i][j]

    added_count = count_added_pairs(original_matrix, closure_matrix)
    print(f"대칭 폐포를 위해 총 {added_count}개의 순서쌍이 추가되었습니다.")
    return closure_matrix


def transitive_closure(matrix):
    original_matrix = [row[:] for row in matrix]
    size = len(matrix)
    tc_matrix = [row[:] for row in matrix]

    for k in range(size):
        for i in range(size):
            for j in range(size):
                tc_matrix[i][j] = tc_matrix[i][j] | (tc_matrix[i][k] & tc_matrix[k][j])

    added_count = count_added_pairs(original_matrix, tc_matrix)
    print(f"추이 폐포를 위해 총 {added_count}개의 순서쌍이 추가되었습니다.")
    return tc_matrix


def get_equivalence_classes(matrix, a):
    size = len(matrix)
    classes = {}

    for i in range(size):
        element = a[i]
        class_list = []
        for j in range(size):
            if matrix[i][j] == 1:
                class_list.append(a[j])

        class_tuple = tuple(sorted(class_list))
        if class_tuple not in classes:
            classes[class_tuple] = True
            print(f"동치류 [{element}]: {set(class_list)}")


def print_matrix(matrix):
    for row in matrix:
        print(row)
    print()


def main():
    a = [1, 2, 3, 4, 5]
    n = len(a)
    matrix = []
    print("5X5 관계 행렬을 행 단위로 입력하세요:")
    for _ in range(n):
        row = list(map(int, input().split()))
        matrix.append(row)

    print()
    print("[관계 R에 포함된 순서쌍]")
    print_relation(matrix, a)
    print()

    current_matrix = [row[:] for row in matrix]

    is_ref = is_reflexive(current_matrix)
    is_sym = is_symmetric(current_matrix)
    is_trans = is_transitive(current_matrix)

    if is_trans and is_sym and is_ref:
        print("이 관계는 동치입니다. 동치류는 다음과 같습니다.")
        get_equivalence_classes(current_matrix, a)
    else:
        print("이 관계는 동치가 아닙니다. 폐포를 추가하여 다시 검사합니다.")

        if is_ref:
            print("\n이 관계는 반사 관계입니다. 반사폐포를 생성할 필요가 없습니다.")
        else:
            print("\n이 관계는 반사 관계가 아닙니다. 반사폐포를 생성합니다.")
            print("반사 폐포 변환 전:")
            print_matrix(current_matrix)
            current_matrix = reflexive_closure(current_matrix)
            print("반사 폐포 변환 후:")
            print_matrix(current_matrix)

        if is_sym:
            print("\n이 관계는 대칭 관계입니다. 대칭폐포를 생성할 필요가 없습니다.")
        else:
            print("\n이 관계는 대칭 관계가 아닙니다. 대칭 폐포를 생성합니다.")
            print("대칭 폐포 변환 전:")
            print_matrix(current_matrix)
            current_matrix = symmetric_closure(current_matrix)
            print("대칭 폐포 변환 후:")
            print_matrix(current_matrix)

        if is_trans:
            print("\n이 관계는 추이 관계입니다. 추이폐포를 생성할 필요가 없습니다.")
        else:
            print("\n이 관계는 추이 관계가 아닙니다. 추이 폐포를 생성합니다.")
            print("추이 폐포 변환 전:")
            print_matrix(current_matrix)
            current_matrix = transitive_closure(current_matrix)
            print("추이 폐포 변환 후:")
            print_matrix(current_matrix)

        final_ref = is_reflexive(current_matrix)
        final_sym = is_symmetric(current_matrix)
        final_trans = is_transitive(current_matrix)

        if final_ref and final_sym and final_trans:
            print("\n폐포를 이용하여 만든 동치 관계 순서쌍은 다음과 같습니다:")
            print_relation(current_matrix, a)
            print("\n동치류는 다음과 같습니다:")
            get_equivalence_classes(current_matrix, a)
        else:
            print(
                "\n경고: 모든 폐포를 적용했으나 동치 관계가 아닙니다. 버그가 발생했습니다."
            )


if __name__ == "__main__":
    main()
