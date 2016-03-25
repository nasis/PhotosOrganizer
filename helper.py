# coding=utf-8
import os

root = r"c:\temp"
input = os.path.sep.join([root, r"hashed_files_list_phase2.txt"])
output = os.path.sep.join([root, r"hashed_files_list_phase3.txt"])
deleted = os.path.sep.join([root, "deleted.txt"])

deleted_paths = [
ur'Z:\Dropbox (Dropbox Team)\תמונות גיבוי\לילך\Card 1\מילי ורינת טסוטת לחול',
ur'Z:\Dropbox (Dropbox Team)\תמונות גיבוי\שיר\שיר- למיין\צופים',
ur'Z:\Dropbox (Dropbox Team)\תמונות גיבוי\-----למיין-----\לילך\מפגש עם שירלי',
ur'Z:\Dropbox (Dropbox Team)\תמונות גיבוי\פייס!',
ur'Z:\Dropbox (Dropbox Team)\תמונות גיבוי\התמונות של גיא\מיטל וגיא',
ur'Z:\Dropbox (Dropbox Team)\תמונות גיבוי\-----למיין-----\כל התמונות מהמצלמה (4G) למחוק מה שיש כבר\114_1612',
ur'Z:\Dropbox (Dropbox Team)\תמונות גיבוי\-----למיין-----\משפחה\102_0603',
ur'Z:\Dropbox (Dropbox Team)\תמונות גיבוי\תמונות מצלמה\102_0603',
ur'Z:\Dropbox (Dropbox Team)\תמונות גיבוי\116_2707',
ur'Z:\Dropbox (Dropbox Team)\תמונות גיבוי\שיר\116_2707',
ur'Z:\Dropbox (Dropbox Team)\תמונות גיבוי\-----למיין-----\כל התמונות מהמצלמה (4G) למחוק מה שיש כבר\113_1512',
ur'Z:\Dropbox (Dropbox Team)\תמונות גיבוי\ברד מטורף באשקלון',
ur'Z:\Dropbox (Dropbox Team)\תמונות גיבוי\115_2607',
ur'Z:\Dropbox (Dropbox Team)\תמונות גיבוי\תמונות מצלמה\101_2805',
ur'Z:\Dropbox (Dropbox Team)\תמונות גיבוי\תמונות מצלמה\103_0703',
ur'Z:\Dropbox (Dropbox Team)\תמונות גיבוי\103_0703',
ur'Z:\Dropbox (Dropbox Team)\תמונות גיבוי\שיר\שיר- למיין\למיין אולי כבר קיים שיר פולין\108NIKON',
ur'Z:\Dropbox (Dropbox Team)\תמונות גיבוי\תיקיה חדשה',
ur'Z:\Dropbox (Dropbox Team)\תמונות גיבוי\שיר\שיר- למיין\תיקיה חדשה',
ur'Z:\Dropbox (Dropbox Team)\תמונות גיבוי\התמונות של גיא\טיול סוכות לים המלח 5-6.10.2007',
ur'Z:\Dropbox (Dropbox Team)\תמונות גיבוי\מצלמה ספטמבר\100_2002',
ur'Z:\Dropbox (Dropbox Team)\תמונות גיבוי\שיר\שיר- למיין\חלק מבולטימורים בארץ',
ur'Z:\Dropbox (Dropbox Team)\תמונות גיבוי\114_2507',
ur'Z:\Dropbox (Dropbox Team)\תמונות גיבוי\115_2607',
ur'Z:\Dropbox (Dropbox Team)\תמונות גיבוי\שיר\שיר- למיין\200 #2',
ur'Z:\Dropbox (Dropbox Team)\תמונות גיבוי\מצלמה ספטמבר\שיר חוזרת מבולטימור ויום הולדת לשיר',
ur'Z:\Dropbox (Dropbox Team)\תמונות גיבוי\שיר\שיר- למיין\עוד חלק מהבולטימורים בארץ',
ur'Z:\Dropbox (Dropbox Team)\תמונות גיבוי\-----למיין-----\כל התמונות מהמצלמה (4G) למחוק מה שיש כבר\111_1312',
ur'Z:\Dropbox (Dropbox Team)\תמונות גיבוי\התמונות של גיא\מסיבת הרווקות של ארז וחן'
]

with open(input) as i:
    input_lines = i.readlines()

output_lines = []
for line in input_lines:
    (hash, path) = eval(line)
    test_path = path
    to_be_deleted = False
    while test_path != u'Z:\\':
        test_path = os.path.dirname(test_path)
        if test_path in deleted_paths:
            to_be_deleted = True
            # print "Deleting: " + test_path
            break
    if not to_be_deleted:
        # print "Keeping: " + str((hash, path))
        output_lines.append((hash, path))

with open(output, "w") as o:
    for line in output_lines:
        print >>o, line