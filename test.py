import snp


@snp.snap('/tmp')
def original(a, b, c):
    return a + b * c


@snp.test('/tmp', '__main__.original')
def modified(a, b, c):
    d = b * c
    return a + d


@snp.test('/tmp', '__main__.original')
def modified_broken(a, b, c):
    d = b * c + 2
    return a + d


if __name__ == '__main__':
    for args in [(2,5,8), (8,8,8)]:
        res_o = original(*args)
        print('Result:', res_o)

        res_m = modified()
        print('Result:', res_m)

        assert res_o == res_m

    try:
        modified_broken()
    except AssertionError:
        print('ok')