"modeling checker"
import unittest
import time
import logging
import subprocess

try:
    import ec602lib
    if ec602lib.VERSION < (1,0):
        print("Please update ec602lib.")
        quit()
except AttributeError:
    print("Please update ec602lib.")
    quit()
except ImportError:
    print("Please install ec602lib in this directory or in your PYTHONPATH.")
    quit()


progname = "modeling.py"

valid_imports = set()

refcode={'lines':50,'words':163}

#
LongAdd = (3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 73, 75, 77, 79, 81, 83, 85, 87, 89, 91, 93, 95, 97, 99, 101, 103, 105, 107, 109, 111, 113, 115, 117, 119, 121, 123, 125, 127, 129, 131, 133, 135, 137, 139, 141, 143, 145, 147, 149, 151, 153, 155, 157, 159, 161, 163, 165, 167, 169, 171, 173, 175, 177, 179, 181, 183, 185, 187, 189, 191, 193, 195, 197, 199, 201, 203, 205, 207, 209, 211, 213, 215, 217, 219, 221, 223, 225, 227, 229, 231, 233, 235, 237, 239, 241, 243, 245, 247, 249, 251, 253, 255, 257, 259, 261, 263, 265, 267, 269, 271, 273, 275, 277, 279, 281, 283, 285, 287, 289, 291, 293, 295, 297, 299, 301, 303, 305, 307, 309, 311, 313, 315, 317, 319, 321, 323, 325, 327, 329, 331, 333, 335, 337, 339, 341, 343, 345, 347, 349, 351, 353, 355, 357, 359, 361, 363, 365, 367, 369, 371, 373, 375, 377, 379, 381, 383, 385, 387, 389, 391, 393, 395, 397, 399, 401, 403, 405, 407, 409, 411, 413, 415, 417, 419, 421, 423, 425, 427, 429, 431, 433, 435, 437, 439, 441, 443, 445, 447, 449, 451, 453, 455, 457, 459, 461, 463, 465, 467, 469, 471, 473, 475, 477, 479, 481, 483, 485, 487, 489, 491, 493, 495, 497, 499, 501, 503, 505, 507, 509, 511, 513, 515, 517, 519, 521, 523, 525, 527, 529, 531, 533, 535, 537, 539, 541, 543, 545, 547, 549, 551, 553, 555, 557, 559, 561, 563, 565, 567, 569, 571, 573, 575, 577, 579, 581, 583, 585, 587, 589, 591, 593, 595, 597, 599, 601, 603, 605, 607, 609, 611, 613, 615, 617, 619, 621, 623, 625, 627, 629, 631, 633, 635, 637, 639, 641, 643, 645, 647, 649, 651, 653, 655, 657, 659, 661, 663, 665, 667, 669, 671, 673, 675, 677, 679, 681, 683, 685, 687, 689, 691, 693, 695, 697, 699, 701, 703, 705, 707, 709, 711, 713, 715, 717, 719, 721, 723, 725, 727, 729, 731, 733, 735, 737, 739, 741, 743, 745, 747, 749, 751, 753, 755, 757, 759, 761, 763, 765, 767, 769, 771, 773, 775, 777, 779, 781, 783, 785, 787, 789, 791, 793, 795, 797, 799, 801, 803, 805, 807, 809, 811, 813, 815, 817, 819, 821, 823, 825, 827, 829, 831, 833, 835, 837, 839, 841, 843, 845, 847, 849, 851, 853, 855, 857, 859, 861, 863, 865, 867, 869, 871, 873, 875, 877, 879, 881, 883, 885, 887, 889, 891, 893, 895, 897, 899, 901, 903, 905, 907, 909, 911, 913, 915, 917, 919, 921, 923, 925, 927, 929, 931, 933, 935, 937, 939, 941, 943, 945, 947, 949, 951, 953, 955, 957, 959, 961, 963, 965, 967, 969, 971, 973, 975, 977, 979, 981, 983, 985, 987, 989, 991, 993, 995, 997, 999, 1001, 1003, 1005, 1007, 1009, 1011, 1013, 1015, 1017, 1019, 1021, 1023, 1025, 1027, 1029, 1031, 1033, 1035, 1037, 1039, 1041, 1043, 1045, 1047, 1049, 1051, 1053, 1055, 1057, 1059, 1061, 1063, 1065, 1067, 1069, 1071, 1073, 1075, 1077, 1079, 1081, 1083, 1085, 1087, 1089, 1091, 1093, 1095, 1097, 1099, 1101, 1103, 1105, 1107, 1109, 1111, 1113, 1115, 1117, 1119, 1121, 1123, 1125, 1127, 1129, 1131, 1133, 1135, 1137, 1139, 1141, 1143, 1145, 1147, 1149, 1151, 1153, 1155, 1157, 1159, 1161, 1163, 1165, 1167, 1169, 1171, 1173, 1175, 1177, 1179, 1181, 1183, 1185, 1187, 1189, 1191, 1193, 1195, 1197, 1199, 1201, 1203, 1205, 1207, 1209, 1211, 1213, 1215, 1217, 1219, 1221, 1223, 1225, 1227, 1229, 1231, 1233, 1235, 1237, 1239, 1241, 1243, 1245, 1247, 1249, 1251, 1253, 1255, 1257, 1259, 1261, 1263, 1265, 1267, 1269, 1271, 1273, 1275, 1277, 1279, 1281, 1283, 1285, 1287, 1289, 1291, 1293, 1295, 1297, 1299, 1301, 1303, 1305, 1307, 1309, 1311, 1313, 1315, 1317, 1319, 1321, 1323, 1325, 1327, 1329, 1331, 1333, 1337, 1342, 1347, 1352, 1357, 1362, 1367, 1372, 1377, 1382, 1387, 1392, 1397, 1402, 1407, 1412, 1417, 1422, 1427, 1432, 1437, 1442, 1447, 1452, 1457, 1462, 1467, 1472, 1477, 1482, 1487, 1492, 1497, 1502, 1507, 1512, 1517, 1522, 1527, 1532, 1537, 1542, 1547, 1552, 1557, 1562, 1567, 1572, 1577, 1582, 1587, 1592, 1597, 1602, 1607, 1612, 1617, 1622, 1627, 1632, 1637, 1642, 1647, 1652, 1657, 1662, 1667, 1672, 1677, 1682, 1687, 1692, 1697, 1702, 1707, 1712, 1717, 1722, 1727, 1732, 1737, 1742, 1747, 1752, 1757, 1762, 1767, 1772, 1777, 1782, 1787, 1792, 1797, 1802, 1807, 1812, 1817, 1822, 1827, 1832, 1837, 1842, 1847, 1852, 1857, 1862, 1867, 1872, 1877, 1882, 1887, 1892, 1897, 1902, 1907, 1912, 1917, 1922, 1927, 1932, 1937, 1942, 1947, 1952, 1957, 1962, 1967, 1972, 1977, 1982, 1987, 1992, 1997, 2002, 2007, 2012, 2017, 2022, 2027, 2032, 2037, 2042, 2047, 2052, 2057, 2062, 2067, 2072, 2077, 2082, 2087, 2092, 2097, 2102, 2107, 2112, 2117, 2122, 2127, 2132, 2137, 2142, 2147, 2152, 2157, 2162, 2167, 2172, 2177, 2182, 2187, 2192, 2197, 2202, 2207, 2212, 2217, 2222, 2227, 2232, 2237, 2242, 2247, 2252, 2257, 2262, 2267, 2272, 2277, 2282, 2287, 2292, 2297, 2302, 2307, 2312, 2317, 2322, 2327, 2332, 2337, 2342, 2347, 2352, 2357, 2362, 2367, 2372, 2377, 2382, 2387, 2392, 2397, 2402, 2407, 2412, 2417, 2422, 2427, 2432, 2437, 2442, 2447, 2452, 2457, 2462, 2467, 2472, 2477, 2482, 2487, 2492, 2497, 2502, 2507, 2512, 2517, 2522, 2527, 2532, 2537, 2542, 2547, 2552, 2557, 2562, 2567, 2572, 2577, 2582, 2587, 2592, 2597, 2602, 2607, 2612, 2617, 2622, 2627, 2632, 2637, 2642, 2647, 2652, 2657, 2662, 2667, 2672, 2677, 2682, 2687, 2692, 2697, 2702, 2707, 2712, 2717, 2722, 2727, 2732, 2737, 2742, 2747, 2752, 2757, 2762, 2767, 2772, 2777, 2782, 2787, 2792, 2797, 2802, 2807, 2812, 2817, 2822, 2827, 2832, 2837, 2842, 2847, 2852, 2857, 2862, 2867, 2872, 2877, 2882, 2887, 2892, 2897, 2902, 2907, 2912, 2917, 2922, 2927, 2932, 2937, 2942, 2947, 2952, 2957, 2962, 2967, 2972, 2977, 2982, 2987, 2992, 2997)

class PolynomialTestCase(unittest.TestCase):
    """unit testing for polynomials"""

    def test_imports(self):
        "a. check the imported modules are allowed"
        file_contents=ec602lib.read_file(progname)
        import_set = ec602lib.get_python_imports(file_contents)
        invalid_imports = import_set - valid_imports
        if invalid_imports:
          self.fail('Invalid imports: {}'.format(" ".join(x for x in invalid_imports)))

    def test_init(self):
        "b. create polynomials from sequences"
        list_p = Polynomial( [5,4,3] )
        tuple_p = Polynomial( (3,4,5) )
        range_p = Polynomial( range(5) ) 
        
        empty_q = Polynomial()
        z = Polynomial([])



    def test_eq(self):
        "c. equal and not equal"
        self.assertEqual(Polynomial([1]),Polynomial([1]))
        self.assertEqual(Polynomial([2,1,0]),Polynomial([2,1,0]))        
        self.assertNotEqual(Polynomial([1,1,0]),Polynomial([2,1,0]))        
        self.assertNotEqual(Polynomial(),Polynomial([2,0,0]))

    def test_eval(self):
        "d. eval"
        p = Polynomial( [5,4,3] )
        self.assertAlmostEqual(31,p.eval(2))
        self.assertAlmostEqual(12,p.eval(1))
        self.assertAlmostEqual(6.25,p.eval(0.5))
        q = Polynomial([3,0,0])
        self.assertAlmostEqual(6.75,q.eval(1.5))

    def test_add(self):
        "e. add"
        q1 = Polynomial([4,1])
        q2 = Polynomial([2,4])
        self.assertEqual(q1 + q2,Polynomial([6,5]))
        self.assertNotEqual(q1 + q2,Polynomial([5,6]))        

    def test_add_consistent(self):
        "f. add same two polynomials twice"
        q1 = Polynomial([4,1])
        q2 = Polynomial([2,4])
        self.assertEqual(q1 + q2,Polynomial([6,5]))
        self.assertEqual(q1 + q2,Polynomial([6,5]),msg="it seems you are modifying one of the operators of +")        

    def test_uneven_add(self):
        "g. add different lengths"
        p1 = Polynomial([4,0,1])
        p2 = Polynomial([2,4])

        self.assertEqual(p1+p2,Polynomial([4,2,5]))




    def test_subtract(self):
        "h. subtract"
        q1 = Polynomial([4,1])
        q2 = Polynomial([2,4])
        p1 = Polynomial([4,0,1])
        p2 = Polynomial([2,4])
        self.assertEqual(q1-q2,Polynomial([2,-3]))

    def test_uneven_sub(self):
        "i. subtract different sizes"
        q1 = Polynomial([4,1])
        q2 = Polynomial([2,4])
        p1 = Polynomial([4,0,1])
        p2 = Polynomial([2,4])
        self.assertEqual(p1-p2,Polynomial([4,-2,-3]))

    def test_floating(self):
        "j. floating point numbers"
        p1 = Polynomial([1.2,0,9.5])
        p2 = Polynomial([0.1,5,1.1])
        self.assertEqual(p1+p2,Polynomial([1.3,5,10.6]))

    def test_Mul(self):
        "k. multiply"
        q1 = Polynomial([4,1])
        q2 = Polynomial([2,4])
        w = q1 * q2
        self.assertEqual(w,Polynomial([8,18,4]))
        self.assertEqual(q1,Polynomial([4,1]))       

    def test_UnevenMul(self):
        "l. multiply different lengths"
        p1 = Polynomial([4,0,1])
        p2 = Polynomial([2,4])
        z = p1 * p2
        self.assertEqual(z,Polynomial([8,16,2,4]))

    def test_Get(self):
        "m. get"
        q1 = Polynomial([4,1])
        p1 = Polynomial([4,0,1])
        self.assertEqual(p1[2],4)
        self.assertEqual(q1[1],4)
        self.assertEqual(q1[1],4) # check it has not changed        

    def test_Get_missing_value(self):
        "n. get with missing"
        p1 = Polynomial([4,0,1])
        self.assertEqual(p1[1],0)                
        self.assertEqual(p1[10],0)
        self.assertEqual(p1[100000],0)        

    def test_Neg_sub(self):
        "o. negative powers"
        q = Polynomial([])
        p = Polynomial([])        

        q[-4] = 2
        p[-5] = 1

        w = p+q
        self.assertEqual(w.eval(2),0.15625)

        z1 = p*q
        z2 = Polynomial([])
        z2[-9] = 2
        self.assertEqual(z1,z2)

    def test_complex(self):
        "p. handle complex coefficients"
        self.assertAlmostEqual(Polynomial([1j,5+2j,6,-0.5j]).eval(0.2j),-0.192+0.62j)

    def test_derivative_pos(self):
        "q. derivatives"
        p1 = Polynomial([4,0,1])        
        self.assertEqual(p1.deriv(),Polynomial([8,0]))
        self.assertEqual(p1.deriv(),Polynomial([8,0]))        

        self.assertEqual(Polynomial([1,2,3,0,5]).deriv(),Polynomial([4,6,6,0]))

    def test_derivative_neg(self):
        "r. negative derivatives"
        z = Polynomial()
        z[-1]=2

        w = Polynomial()
        w[-2]=-2
        self.assertEqual(z.deriv(),w)

    def test_Limits(self):
        "s. polynomial unlimited in size"
        longpoly = Polynomial([1]*10000)
        self.assertAlmostEqual(longpoly.eval(1),10000)

    def test_speed(self):
        "t. efficient multiply "

        q = Polynomial()
        p = Polynomial()
        q[440]=1
        q[0]=1
        p[460]=2
        p[0]=3
        w= Polynomial()
        w[900] = 2
        w[440] = 3
        w[460] = 2
        w[0] = 3
        st = time.time()

        self.assertEqual(p*q,w)

        multiply_time = time.time() -st
        if multiply_time>0.0001:
            logging.info('inefficient multiply')
            self.fail("Your multiply is not efficient")


    def test_sparse(self):
        "u. efficiency with lots of zeros."
        q = Polynomial()
        p = Polynomial()
        w = Polynomial()
        q[20000]= 5
        q[10000] = 1
        
        p[30000] = 4
        p[1] = 3

        w[50000] = 20
        w[40000] = 4
        w[10001] = 3
        w[20001] = 15

        st = time.time()

        self.assertEqual(p*q,w)

        multiply_time = time.time() -st
        if multiply_time>0.0001:
            self.fail("Your multiply is not efficient")

    def test_add_long(self):
        "v. long polynomials add efficiency"

        g = list(range(2,1000,3))
        h = list(range(3,2000,2))
        tot = Polynomial(g)+Polynomial(h)
        st = time.time()

        self.assertEqual(tot,Polynomial(LongAdd))

        add_time = time.time() - st
        if add_time>0.002:
            self.fail("Your add is not efficient")

    def test_nomods(self):
        "w. input sequence independent of created polynomial"
        L = [3,2,1]
        p = Polynomial(L)
        L.clear()
        self.assertEqual(p,Polynomial([3,2,1]),msg="you must not link to the sequence")
        L = [2,1]
        p = Polynomial(L)
        p[1]=3
        self.assertEqual(L,[2,1],msg="you must not modify the passed sequence")



if __name__=="__main__":
    from modeling import Polynomial
    _,results,_ = ec602lib.overallpy(progname,PolynomialTestCase,refcode)
    #unittest.main()
    print(results)