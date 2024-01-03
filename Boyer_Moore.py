from Algorithms.Z_Algorithm import z_algo, z_suffix


def BM(txt, pat):
    # init

    alpha = 26  # total number of alphabets (only small characters)
    A = ord('a')  # ascii value of 'a' for ascii calculations
    m = len(pat)  # length of pat
    n = len(txt)  # length of txt

    matches = []  # list of indices where pattern is found

    # pattern is just one letter, no need to preprocess anything
    if m == 0 or n == 0:
        return matches

    elif m == 1:
        c = ord(pat)
        for i in range(n):
            if c == ord(txt[i]):
                matches.append(i)

        return matches

    # Preprocess ebc, z, gs, mp

    ebc = bad_character(pat, m, alpha)

    # ebc = calc_extended_bad_char(pat)

    z_arr = z_suffix(pat)

    gs = good_suffix(z_arr, m)
    print(f'gs: {gs}')
    # gs = goodsuf(pat)

    mp = matched_prefix(z_arr, m)
    print(f'mp: {mp}')
    # mp = matchedprefix(pat)
    # return
    # print('Printing EBC:')
    # for l in ebc:
    #     print(l)
    # print('--------------------------------------------------')
    # print(f'Z Array:\n {z_arr}')
    # print(f'Good suffix:\n {gs}')
    # print(f'Matched prefix:\n {mp}')

    # iterate txt from left to right based on shifts
    txt_i = 0
    stop = -1
    start = -1

    while (txt_i + m - 1) < n:
        fullmatch = True  # full match flag
        pat_i = m - 1  # iterate pat from right to left
        n_bc = 0  # shifts from bad character rule
        n_gs = 0  # shifts from good suffix rule
        print(f'\nNew Loop... {txt_i}')
        while fullmatch and (pat_i >= 0):
            # print(pat_i)
            # print(start)
            pat_c = ord(pat[pat_i])  # ascii val of current pat char
            txt_c = ord(txt[txt_i + pat_i])  # ascii val of current txt char
            print(f'pat: {chr(pat_c)} txt: {chr(txt_c)}')

            # match -> continue
            if pat_c == txt_c:
                # skip this substring as per galil's optimization
                if pat_i == stop and start < stop:
                    # print('here')
                    print(f'from: {stop} to: {start} pat_i: {pat_i}')
                    pat_i = start + 1

                pat_i -= 1

            # mismatch -> determine shifts based on bc and gs rules
            else:
                print(f'pat: {pat_i}')
                fullmatch = False  # pattern doesn't exist here
                # BC    
                p = ebc[pat_i][txt_c - A]

                print(f'BC p: {p}')

                # if p < pat_i:
                n_bc = pat_i - p
                print(f'BC - n_bc: {n_bc}')

                # else:
                #     print(f'BC 2 - n_bc: {n_bc}')
                #     n_bc = 1

                # GS
                p = gs[pat_i + 1]  # last index of next rightmost alpha
                # Case 1a
                if p >= 0:
                    n_gs = m - p - 1
                    stop = p
                    start = p - m + pat_i + 1
                    print(f'GS 1a - p: {p} n_gs: {n_gs}')

                # Case 1b
                else:
                    n_gs = m - mp[pat_i + 1]
                    stop = mp[pat_i + 1] - 1
                    start = 0
                    print(f'GS 1b - p: {p} n_gs: {n_gs}')

        # Case 2: full match
        if fullmatch:
            print("MP 3")
            matches.append(txt_i)
            n_gs = m - mp[1]
            stop = mp[1] - 1
            start = 0

        shift = max(n_bc, n_gs)
        # start = pat_i - 1
        # stop = pat_i + n_gs
        print(f'shift: {shift}')
        txt_i += shift

    return matches


"""
PREPROCESSING FUNCTIONS
"""


# def z_algo_suffix(input):
#     n = len(input)
#     zValues = [0 for i in range(n)]
#     zValues[n - 1] = n
#
#     prefix_index = n - 1
#     z_index = n - 2
#     z_score_current = 0
#     while z_index >= 0 and input[prefix_index] == input[z_index]:
#         z_score_current += 1
#         z_index -= 1
#         prefix_index -= 1
#     zValues[n - 2] = z_score_current
#     if z_score_current > 0:
#         r = n - 2 - (z_score_current - 1)
#         l = n - 2
#     else:
#         r = n - 1
#         l = n - 1
#
#     for k in range(n - 3, -1, -1):
#         if k < r:
#             prefix_index = n - 1
#             z_index = k
#             z_score_current = 0
#             while z_index >= 0 and input[prefix_index] == input[z_index]:
#                 z_score_current += 1
#                 z_index -= 1
#                 prefix_index -= 1
#             if z_score_current > 0:
#                 r = k - (z_score_current - 1)
#                 l = k
#             zValues[k] = z_score_current
#         else:
#             # If the z value of the similar box less
#             # than the length....
#             if zValues[n - 1 - (l - k)] < k - r + 1:
#                 zValues[k] = zValues[n - 1 - (l - k)]
#             else:
#                 if zValues[n - 1 - (l - k)] > k - r + 1:
#                     zValues[k] = k - r + 1
#                 else:
#                     z_index = r - 1
#                     prefix_index = n - 1 - (k - r + 1)
#                     while z_index >= 0 and input[prefix_index] == input[z_index]:
#                         z_score_current += 1
#                         z_index -= 1
#                         prefix_index -= 1
#                     zValues[k] = k - z_index
#                     r = z_index + 1
#                     l = k
#     return zValues

# def matchedprefix(pat):
#     z_score = z_algo(pat)
#     matched = [0 for i in range(len(pat) + 1)]
#     for i in range(len(pat) - 1, -1, -1):
#         z_score_current = z_score[i]
#         prev = matched[i + 1]
#         if i + z_score_current >= len(pat):
#             matched[i] = max(prev, z_score_current)
#         else:
#             matched[i] = prev
#     return matched

# def goodsuf(pat):
#     good_suffix = [0 for i in range(len(pat) + 1)]
#     z = z_suffix(pat)
#     for i in range(1, len(pat)):
#         j = len(pat) - z[i - 1] + 1
#         good_suffix[j - 1] = i
#     return good_suffix


def bad_character(pat, n, alpha):
    ebc = []

    for _ in range(n):
        ebc.append([-1] * alpha)

    a = ord('a')

    for row in range(1, n):
        # current alphabet from pat
        c = ord(pat[row - 1])

        for col in range(alpha):
            if (a + col) == c:
                ebc[row][col] = row - 1

            else:
                ebc[row][col] = ebc[row - 1][col]

    return ebc


def good_suffix(z_arr, n):
    # print(n)
    gs = [-1] * (n + 1)

    for p in range(n-1):
        pat_i = n - z_arr[p] + 1
        gs[pat_i-1] = p

    return gs


def matched_prefix(z_arr, n):
    mp = [0] * (n + 1)

    z_i = 0
    mp_i = n - 1

    while z_i < n and mp_i >= 0:

        if z_arr[z_i] == z_i + 1:
            mp[mp_i] = z_arr[z_i]

        else:
            mp[mp_i] = mp[mp_i + 1]

        z_i += 1
        mp_i -= 1

    return mp

def find_wildcard(pat):
    m = len(pat)
    wc = '.'
    wc_i = -1

    if m % 2 == 1:
        if pat[m//2] == wc:
            wc_i = m//2

    if wc_i == -1:
        i = 0
        j = m-1
        while i < j:
            if pat[i] == wc:
                wc_i = i
                break
            elif pat[j] == wc:
                wc_i = j
                break
            i += 1
            j -= 1

    return wc_i

# BC preprocessing with wildcard
def bad_character_wc(pat, n, alpha, wc_i):
    ebc = []

    for i in range(n):
        if i == wc_i+1:
            # instead of adding one more slot for wildcard, just sub as previous row (since every letter exists at this index)
            ebc.append([i-1] * alpha)
        else:
            ebc.append([-1] * alpha)

    a = ord('a')

    for row in range(1, n):
        # current alphabet from pat
        c = ord(pat[row - 1])

        if row == wc_i+1:
            continue

        for col in range(alpha):
            if (a + col) == c:
                ebc[row][col] = row - 1

            else:
                ebc[row][col] = ebc[row - 1][col]

    return ebc

def z_suf_wc(txt, wc_i):
    n = len(txt)
    zValues = [0] * n
    zValues[n - 1] = n

    # init start indices and z score
    suf_i = n - 1
    z_i = n - 2
    z_k = 0
    suf_i, z_i, z_k = z_suf_compare_wc(txt, suf_i, z_i, z_k, wc_i)

    # base case - init z box with second last letter
    zValues[n - 2] = z_k
    if z_k > 0:
        l = n - (z_k - 1) - 2
        r = n - 2

        # if wildcard exists in zbox, cut z box to l = wildcard+1
        if r == wc_i: # wildcard is right end of z box, so this z box should not be used
            l = n - 1
            r = n - 1

        elif l <= wc_i:
            l = wc_i + 1

    else:
        l = n - 1
        r = n - 1

    # start from Z3
    k = n - 3
    while k >= 0:
        z_k = 0
        # case 1
        if k < l:
            # set indices
            suf_i = n - 1
            z_i = k

            # pattern match and update indices
            suf_i, z_i, z_k = z_suf_compare_wc(txt, suf_i, z_i, z_k, wc_i)

            # if found, update z box
            if z_k > 0:
                l = z_i + 1
                r = k
                # if wildcard exists in zbox, cut z box to l = wildcard+1
                if r == wc_i:
                    l = n - 1
                    r = n - 1

                elif l <= wc_i:
                    l = wc_i + 1

            zValues[k] = z_k

        # case 2
        else:
            # extra case: if z values doesnt exceed z box
            if zValues[(r - k + 1) * -1] < k - l + 1:
                zValues[k] = zValues[(r - k + 1) * -1]

            else:
                # case 2a
                if zValues[(r - k + 1) * -1] > k - l + 1:
                    zValues[k] = k - l + 1
                # case 2b
                else:
                    # set z and prefix indices
                    z_i = l - 1
                    suf_i = n - (k - l + 1) - 1

                    # do pattern match and update indices
                    suf_i, z_i, z_k = z_suf_compare_wc(txt, suf_i, z_i, z_k, wc_i)
                    # update z box and z_k
                    zValues[k] = k - z_i
                    l = z_i + 1
                    r = k
                    # if wildcard exists in zbox, cut z box to l = wildcard+1
                    if r == wc_i:
                        l = n - 1
                        r = n - 1

                    elif l <= wc_i:
                        l = wc_i + 1

        k -= 1

    return zValues

def z_suf_compare_wc(txt, suf_i, z_i, z_k, wc_i):
    while z_i >= 0 and (txt[suf_i] == txt[z_i] or z_i == wc_i or suf_i == wc_i):
        z_k += 1
        suf_i -= 1
        z_i -= 1

    return suf_i, z_i, z_k

def boyer_moore(txt, pat):
    # init
    alpha = 26  # total number of alphabets (only small characters)
    A = ord('a')  # ascii value of 'a' for ascii calculations
    m = len(pat)  # length of pat
    n = len(txt)  # length of txt

    matches = []  # list of indices where pattern is found

    wc_i = find_wildcard(pat)
    print(wc_i)

    # pattern is just one letter, no need to preprocess anything
    if m == 0 or n == 0:
        return matches

    # wildcard is the only pat, so everything matches
    elif m == 1 and m == wc_i-1:
        return [i for i in range(n)]

    elif m == 1:
        c = ord(pat)
        for i in range(n):
            if c == ord(txt[i]):
                matches.append(i)

        return matches

    # Preprocess ebc, z, gs, mp

    ebc = bad_character_wc(pat, m, alpha,wc_i)

    z_arr = z_suf_wc(pat, wc_i)

    gs = good_suffix(z_arr, m)

    mp = matched_prefix(z_arr, m)
    # return
    print('Printing EBC:')
    for l in ebc:
        print(l)
    print('--------------------------------------------------')
    print(f'Z Array:\n {z_arr}')
    print(f'Good suffix:\n {gs}')
    print(f'Matched prefix:\n {mp}')

    # iterate txt from left to right based on shifts
    txt_i = 0
    stop = -1
    start = -1
    # print(wc_i)
    while (txt_i + m - 1) < n:
        fullmatch = True  # full match flag
        pat_i = m - 1  # iterate pat from right to left
        n_bc = 0  # shifts from bad character rule
        n_gs = 0  # shifts from good suffix rule
        print(f'\nNew Loop... {txt_i}')
        while fullmatch and (pat_i >= 0):
            # print(pat_i)
            # print(start)
            pat_c = ord(pat[pat_i])  # ascii val of current pat char
            txt_c = ord(txt[txt_i + pat_i])  # ascii val of current txt char
            print(f'pat: {chr(pat_c)} txt: {chr(txt_c)}')

            # match -> continue
            if pat_c == txt_c or pat_i == wc_i:
                # skip this substring as per galil's optimization
                if pat_i == stop and start < stop:
                    # print('here')
                    print(f'from: {stop} to: {start} pat_i: {pat_i}')
                    pat_i = start + 1

                pat_i -= 1

            # mismatch -> determine shifts based on bc and gs rules
            else:
                print(f'pat: {pat_i}')
                fullmatch = False  # pattern doesn't exist here
                # BC
                p = ebc[pat_i][txt_c - A]

                print(f'BC p: {p}')

                # if p < pat_i:
                n_bc = pat_i - p
                # print(f'BC 1 - n_bc: {n_bc}')

                # if p == wc_i:
                #     print(f'BC 1 - n_bc: {n_bc}')
                #     stop = -1
                #     start = -1
                #     break

                print(f'BC 1 - n_bc: {n_bc}')
                # GS
                p = gs[pat_i + 1]  # last index of next rightmost alpha
                # Case 1a
                if p > 0:
                    n_gs = m - p - 1
                    print('Galil 1a')
                    stop = p - m + pat_i - 1
                    start = p
                    print(f'GS 1a - p: {p} n_gs: {n_gs}')

                # Case 1b
                elif p == -1:
                    n_gs = m - mp[pat_i + 1] - 1
                    stop = mp[pat_i + 1] - 1
                    start = 0
                    print(f'GS 1b - p: {p} n_gs: {n_gs}')

                else:
                    n_gs = 1
                    print(f'GS 1c - p: {p} n_gs: {n_gs}')

                # else:
                    # n_gs = 1

        # Case 2: full match
        if fullmatch:
            print("MP 3")
            matches.append(txt_i)
            n_gs = m - mp[1]
            stop = mp[1] - 1
            start = 0

        shift = max(n_bc, n_gs)
        # start = pat_i - 1
        # stop = pat_i + n_gs
        print(f'shift: {shift}')
        txt_i += shift

    return matches

if __name__ == '__main__':
    pat = "aabacabacaba"
    pat1 = "acababacaba"
    pat2 = "acababacababacaba"
    pat3 = "tbapxab"
    pat4 = "acaba"
    txt = "xpbctbxabtbapxabbpqa"
    txt2 = "bbbbabbbbbbabb"
    pat5 = "bbbbbbbbbbbbbbbbbb"
    txt3 = "aaaaaaaaaa"
    pat6 = "aaa"
    pat7 = 'bbabacacbacbaacacbbb'
    pat8 = 't.t'
    # text10 = 'aagacacataaagaagctttataacgtcaaggtcgcaaggcactacctattgctccccgacggttaaggttagcagctccactcccgcggaataggtacgaattatgagtgactgatttttctggtacccgggcaagagcctaaactgagcgaaacattttcattcctggctgaagatgttcatagcgtccacctcggttggccgttattccagcactggagaacaccggtcaaccaattggccactgtgcacgcgtcgttcggctgtggaagcggcggaactgacgaatagtttacctggctgtactgaacgtacacccgtctgccgttgttgttaatccattgtgccaatttagctcaccgagtcacgcgacactctgggcttgagaggcgggcgagtggttcacatggcgcggagtgtagtttgtgagatattctaggaagaacgtcgttgctaggtcacggcacagatacaggatccatacaatagttagctagcctggatggacttattctcatattgcttgtgagcagcctttaaagtggggtctacagaagtcagtaggcttatgtcgcggaaccggggccacgcgagatctaatacggttgcgaagggcgtcttatcagcgggatactgagccaatggcagtgataattccgtaggttctataagtcgggtatcagcgaccgcctagccatacccgaaatgtcggcattcctcggcaacgaacgaccatgaaccgctaagaagcgacgagccgaatcagatccggacaccgcgacccctcaactccgggctttctgagcatgaagcgtgctacatcgattttgaagtgaaagatactgggtggcgccgagtatgagtaggaggaccacatggagctttgaagatggtatttaaccccggggttatggacctcctaccggccttccgggttcgtagtcgaaggttgtccatacaggtttcgtttttgtcaaccgagcccggcaagcagtacga'
    # pat10 = 'g.cac'

    # z = z_algo(pat2[::-1])
    # z.reverse()
    # z = z_algo(pat7)
    # suf = z_suffix(pat10)
    # print(z)
    # print(suf)
    # print(good_suffix(suf, len(pat8)))
    # print(matched_prefix(suf, len(pat8)))
    # print(len(pat5))
    # n = len(pat1)
    # print(f'GS: {good_suffix(z, n)}\nMP: {matched_prefix(z, n)}')
    # print(BM(text10, pat10))
    # wc_i = find_wildcard(pat8)
    txt = 'actcaagatacaggctcggtaacgtacgctctagccatctaactatcccctatgtcttatagggacctacgttatctgcctgtcgaaccataggattcgcatcagcgcgcaggcttgggtcgagataaaatctccagtgcccaagaccacgggcgctcggcgtcttggctaatccccgtacatgttgttataaataatcagtagaaactctgtgttagagggtggagtgaccttaaatcaaggacgatattaatcggaaggagtattcaacgtgatgaagtcgcagggttgacgtgggaatggtgcttctgtccaaacaggttagggtataacgccggaaccgtcccccaagcgtacagggtgggctttgcaacgacttccgagtccaaagactcgctgttttcgaaatttgcgctcaagggcgagtattgaaccaggcttacgcccaagtacgtagcaaggtgactcaaacagagtacatcctgcccgcgtttcgtatg'
    pat = 'tat.tg'
    pat1 = 'acababacaba'
    print(boyer_moore(txt, pat))
    # print(wc_i)
    # ebc = bad_character_wc(pat8, len(pat8), 26, wc_i)
    #
    # for c in ebc:
    #     print(c)
