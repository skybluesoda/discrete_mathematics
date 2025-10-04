import time


def get_matrix_determinant(m):
    if len(m) == 1:
        return m[0][0]
    if len(m) == 2:
        return m[0][0] * m[1][1] - m[0][1] * m[1][0]

    det = 0
    for c in range(len(m)):
        det += ((-1) ** c) * m[0][c] * get_matrix_determinant(get_matrix_minor(m, 0, c))

    return det


def get_matrix_minor(m, i, j):
    return [row[:j] + row[j + 1 :] for row in (m[:i] + m[i + 1 :])]


def has_inverse(m):
    det = get_matrix_determinant(m)
    if abs(det) < 1e-10:
        print("행렬식이 0이므로 역행렬 계산이 불가능합니다.")
        return False
    return True


def transpose_matrix(m):
    return [[m[j][i] for j in range(len(m))] for i in range(len(m[0]))]


def get_matrix_inverse(m):
    determinant = get_matrix_determinant(m)

    if len(m) == 1:
        return [[1.0 / m[0][0]]]

    if len(m) == 2:
        return [
            [m[1][1] / determinant, -1 * m[0][1] / determinant],
            [-1 * m[1][0] / determinant, m[0][0] / determinant],
        ]

    cofactors = []
    for r in range(len(m)):
        cofactor_row = []
        for c in range(len(m)):
            minor = get_matrix_minor(m, r, c)
            cofactor_row.append(((-1) ** (r + c)) * get_matrix_determinant(minor))
        cofactors.append(cofactor_row)

    adjugate = transpose_matrix(cofactors)

    for r in range(len(adjugate)):
        for c in range(len(adjugate)):
            adjugate[r][c] = adjugate[r][c] / determinant

    return adjugate


def matrix_out(mx, size):
    print("「" + "       " * size + "ㄱ")
    for i in range(size):
        print("|", end=" ")
        for j in range(size):
            print("%7.3f" % mx[i][j], end=" ")
        print("|")
    print("L" + "       " * size + "」")


def is_identical(m, n):
    for i in range(len(m)):
        for j in range(len(m[0])):
            if abs(m[i][j] - n[i][j]) > 1e-10:
                return False
    return True


def unit_matrix(size):
    m = [[0 for _ in range(size)] for _ in range(size)]
    for i in range(size):
        m[i][i] = 1
    return m


def gauss_jordan(m):
    aug = [row1 + row2 for row1, row2 in zip(m, unit_matrix(len(m[0])))]
    for i in range(len(m[0])):
        if aug[i][i] < 1e-10:
            for j in range(i + 1, len(m[0])):
                if abs(aug[j][i]) > 1e-10:
                    aug[i], aug[j] = aug[j], aug[i]
                    break
        dividend = aug[i][i]
        for j in range(2 * len(m[0])):
            aug[i][j] /= dividend
        for j in range(len(m[0])):
            if i != j:
                factor = aug[j][i]
                for k in range(2 * len(m[0])):
                    aug[j][k] -= factor * aug[i][k]
    inverse = [row[len(m[0]) :] for row in aug]
    return inverse


def main():
    try:
        k = int(input("정방행렬의 차수를 입력하시오: "))
        if k <= 0:
            print("차수는 양의 정수여야 합니다.")
            return
        print(
            f"{k}x{k} 정방행렬 A를 입력하세요 (각 행을 공백으로 구분하여 한 줄씩 입력):"
        )
        matrix_a = []
        for i in range(k):
            while True:
                try:
                    row_input = input(f"{i+1}행: ").strip()
                    row_values = [float(x) for x in row_input.split()]
                    if len(row_values) != k:
                        print(f"입력 오류: 정확히 {k}개의 값을 입력해야 합니다.")
                        continue
                    matrix_a.append(row_values)
                    break
                except ValueError:
                    print("입력 오류: 숫자만 입력해주세요.")
        if has_inverse(matrix_a):
            print("행렬식을 이용해 계산된 역행렬은 다음과 같습니다:")
            det_start = time.time()
            inverse_det = get_matrix_inverse(matrix_a)
            det_end = time.time()
            det_time = det_end - det_start
            matrix_out(inverse_det, k)
            print("가우스-조던 소거법을 이용해 계산된 역행렬은 다음과 같습니다:")
            gj_start = time.time()
            inverse_gj = gauss_jordan(matrix_a)
            gj_end = time.time()
            gj_time = gj_end - gj_start
            matrix_out(inverse_gj, k)
        if is_identical(inverse_det, inverse_gj):
            print("두 방법으로 계산된 역행렬이 동일합니다.")
            print(f"또한, 행렬식을 이용한 계산에선 {det_time:.6f}초의 시간이,")
            print(f"가우스-조던 소거법을 이용한 계산에선 {gj_time:.6f}초의 시간이 소요되었습니다.")
        else:
            print("두 방법으로 계산된 역행렬이 동일하지 않습니다.")

    except ValueError:
        print("입력 오류: 정수를 입력해주세요.")
    except Exception as e:
        print(f"예상치 못한 오류가 발생했습니다: {e}")
    print()


if __name__ == "__main__":
    main()
