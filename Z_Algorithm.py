import time


def z_algo(str_in=""):
    # initialize list of z values
    n = len(str_in)
    zValues = [0] * n
    zValues[0] = n

    # empty str/only 1 char, no pattern
    if n < 2:
        return zValues

    # initialize starting indices and current z score
    prefix_idx = 0
    z_idx = 1
    z_k = 0
    prefix_idx, z_idx, z_k = compare(str_in, prefix_idx, z_idx, z_k)

    # base case - initialize current z box indices
    zValues[1] = z_k

    if z_k > 0:
        r = z_k
        l = 1

    else:
        r = 0
        l = 0

    # start from Z3
    for k in range(2, n):
        # case 1
        z_k = 0
        if k > r:
            # set current z score indices
            prefix_idx = 0
            z_idx = k

            # update indices and score after pattern matching
            prefix_idx, z_idx, z_k = compare(str_in, prefix_idx, z_idx, z_k)
            # update z box indices if found pattern
            if z_k > 0:
                r = z_idx - 1
                l = k

            zValues[k] = z_k
        # case 2
        else:
            # extra case: if z value does not exceed current z box length
            if zValues[k - l] < r - k + 1:
                zValues[k] = zValues[k - l]

            else:
                # case 2a
                if zValues[k - l] > r - k + 1:
                    zValues[k] = r - k + 1
                # case 2b
                else:
                    # set z and prefix indices
                    z_idx = r + 1
                    prefix_idx = r - k + 1

                    # update indices and score after pattern matching
                    prefix_idx, z_idx, z_k = compare(str_in, prefix_idx, z_idx, z_k)
                    # update current z value and box indices
                    zValues[k] = z_idx - k
                    r = z_idx - 1
                    l = k

    return zValues


def z_suffix(str_in):
    # print(str_in)
    STR_LEN = len(str_in)
    # print(STR_LEN)
    zValues = [0] * STR_LEN
    zValues[STR_LEN - 1] = STR_LEN

    # empty str/only 1 char, no pattern
    if STR_LEN < 2:
        return zValues

    # initialize starting indices and current z score
    suffix_idx = STR_LEN - 1
    z_idx = STR_LEN - 2
    z_k = 0
    suffix_idx, z_idx, z_k = compare_suffix(str_in, suffix_idx, z_idx, z_k)

    zValues[STR_LEN - 2] = z_k
    # if zValues[STR_LEN - 2] == STR_LEN - 1:  # this means all letter in pat are the same
    #     for i in range(STR_LEN - 2):
    #         zValues[i] = i + 1
    #     return zValues
    # base case - initialize current z box indices
    if z_k > 0:
        l = STR_LEN - (z_k - 1) - 2
        r = STR_LEN - 2

    else:
        l = STR_LEN - 1
        r = STR_LEN - 1

    # start from Z3
    k = STR_LEN - 3
    while k >= 0:
        z_k = 0
        # case 1
        if k < l:
            # set current z score indices
            suffix_idx = STR_LEN - 1
            z_idx = k

            # update indices and score after pattern matching
            suffix_idx, z_idx, z_k = compare_suffix(str_in, suffix_idx, z_idx, z_k)

            # update z box indices if found pattern
            if z_k > 0:
                l = z_idx + 1
                r = k

            zValues[k] = z_k

        # case 2
        else:
            # extra case: if z value does not exceed current z box length
            if zValues[(r - k + 1) * -1] < k - l + 1:
                zValues[k] = zValues[(r - k + 1) * -1]

            else:
                # case 2a
                if zValues[(r - k + 1) * -1] > k - l + 1:
                    zValues[k] = k - l + 1
                # case 2b
                else:
                    # set z and prefix indices
                    z_idx = l - 1
                    suffix_idx = STR_LEN - (k - l + 1) - 1

                    # update indices and score after pattern matching
                    suffix_idx, z_idx, z_k = compare_suffix(str_in, suffix_idx, z_idx, z_k)
                    # update current z value and box indices
                    zValues[k] = k - z_idx
                    l = z_idx + 1
                    r = k

        k -= 1

    return zValues


def compare(str_in, prefix_idx, z_idx, z_k):
    n = len(str_in)

    while z_idx < n and str_in[prefix_idx] == str_in[z_idx]:
        z_k += 1
        prefix_idx += 1
        z_idx += 1
    return z_k, z_idx, prefix_idx


def compare_suffix(str_in, suffix_idx, z_idx, z_k):
    # z = z_idx
    # score = z_k
    while z_idx >= 0 and str_in[suffix_idx] == str_in[z_idx]:
        z_k += 1
        suffix_idx -= 1
        z_idx -= 1
    return suffix_idx, z_idx, z_k


def naiveZ(str_in: str = "") -> list[int]:
    # initialize values
    n = len(str_in)
    zValues = [n]
    numMatches = 0
    # initialize return array
    for _ in range(n - 1):
        zValues.append(0)
    # compare each letter within str_in starting from index i
    for i in range(1, n):
        numMatches = compare_naive(str_in, i)
        zValues[i] = numMatches

    return zValues


def compare_naive(str_in="", i=0, j=0):
    # initialize
    n = len(str_in)
    matches = 0
    # start comparing
    while i < n and j < n:
        if str_in[i] == str_in[j]:
            matches += 1
            i += 1
            j += 1
        else:
            break

    return matches


def concat(txt, pat, prefix):
    # If true, concat in front, if false, concat at the back
    if prefix:
        str_out = ''.join([pat, chr(36),
                           txt])  # selected '$' as the separation between pat and txt since it is out of the ascii range
    else:
        str_out = ''.join([txt, chr(36), pat])

    print(str_out)

    return str_out


if __name__ == '__main__':
    # test_in = ["ababc", "aabxaabxdaabeewwdaabxaabxdabaabxaax", "eeebbbwweeebbbewidfoewfnweeebbbssssseessvveeebbbwweeebbbewidfoewfnweeebbbssssseessvv", "a"]
    # for s in test_in:
    #     print(naiveZ(s) == z_algo(s))
    test = "aabacabacaba"
    pat = "aabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacabaaabacabacaba"
    pat1 = "acababacaba"
    pat2 = "acababacababacabaabhabhabhabadbabababbaaabccbaccacacabcacaacbajdasbjsoajcabcacacabcabcababcabcacbababcabcbahcjdbsalfherjqofnwuioncjevnfrejsvf"
    pat3 = "tbapxab"
    pat4 = "acaba"
    pat5 = "bbbb"
    # print(z_algo("bbbbbabbbbbbbbbbbb"))
    # z = z_algo(pat5[::-1])
    # z.reverse()
    # print(z)
    # start = time.time()
    # print(naiveZ(pat))
    # print(f'{time.time()-start}')
    # start = time.time()
    # print(z_algo(pat))
    # print(f'{time.time()-start}')
    # start = time.time()
    # print(z_suffix(pat))
    # print(f'{time.time()-start}')
    # print(z_algo(test))
    pat = 'alpesss'
    txt = 'cdlapesss'
    pat2 = 'caa'
    txt2 = 'caaacaac'
    z_pre = z_algo(concat(txt2, pat2,
                          True))  # concatenate current pat in front of current txt, then create prefix z array    O(2(N+M))
    z_suf = z_suffix(concat(txt2, pat2,
                            False))  # concatenate current pat at the back of current txt, then create suffix z array O(2(N+M))
    res = [None]
    m = len(pat2)
    j = m - 1
    counter = 0
    for i in range(m + 1, len(z_pre) - m + 1):
        if z_pre[i] == m:
            res.append((i - m, -1))
            counter += 1
        elif z_pre[i] + z_suf[j] == m - 2:
            # comment
            if txt2[i-m+1] == pat2[z_pre[i]] and txt2[i-m] == pat2[z_pre[i+1]]:
                res.append((i - m, i - m + z_pre[i]))
                counter += 1
        j += 1

    res[0] = counter
    print(res[0])
    for i in range(1, len(res)):
        str_out = f'{res[i][0]}'
        if res[i][1] > -1:
            str_out += f' {res[i][1]}'
        print(str_out)

    # print(z_pre)
    print(z_pre[len(pat2) + 1::])
    # print(z_suf)
    print(z_suf[:-len(pat2) - 1])
    # print(z_suf[-len(pat)-2])

    # concat pat with txt
    # z pre/suf with pattxt
    # iterate z pre compare with z suf
    # if z_pre[i]+z_suf[z_pre(i)+len] = len(pat) TRUE


# z algorithm that traverses from txt[-1] to txt[0], giving a z array with z scores by comparing suffix
# def z_suf(txt):
#     print(txt)
#     # init z array
#     n = len(txt)
#     print(n)
#     z_val = [0] * n
#     z_val[n - 1] = n
#
#     # init start indices and z score
#     suf_i = n - 1
#     z_i = n - 2
#     z_k = 0
#     suf_i, z_i, z_k, z_suf_compare(txt, suf_i, z_i, z_k)
#
#     # base case - init z box with second last letter
#     z_val[n - 2] = z_k
#     if z_k > 0:
#         l = n - (z_k - 1) - 2
#         r = n - 2
#
#     else:
#         l = n - 1
#         r = n - 1
#
#     k = n - 3
#     while k >= 0:
#         z_k = 0
#         # case 1
#         if k < l:
#             # set indices
#             suf_i = n - 1
#             z_i = k
#
#             # pattern match and update indices
#             suf_i, z_i, z_k = z_suf_compare(txt, suf_i, z_i, z_k)
#
#             # if found, update z box
#             if z_k > 0:
#                 l = z_i + 1
#                 r = k
#
#             z_val[k] = z_k
#
#         # case 2
#         else:
#             # if z values doesnt exceed z box
#             if z_val[(r - k + 1) * -1] < k - l + 1:
#                 z_val[k] = z_val[(r - k + 1) * -1]
#
#             else:
#                 # case 2a
#                 if z_val[(r - k + 1) * -1] > k - l + 1:
#                     z_val[k] = k - l + 1
#                 # case 2b
#                 else:
#                     z_i = l - 1
#                     suf_i = n - (k - l + 1) - 1
#
#                     # do pattern match and update indices
#                     suf_i, z_i, z_k = z_suf_compare(txt, suf_i, z_i, z_k)
#
#
#                     z_val[k] = k - z_i
#                     l = z_i + 1
#                     r = k
#
#         k -= 1
#
#     return z_val