import pandas as pd
import sys


def main():
    # first arg should be the name of the csv to read in
    filename = sys.argv[1]
    start_num = int(sys.argv[2])  # second is the line we start at.
    end_num = int(sys.argv[3])  # the line we end at

    df = pd.read_csv(filename)

    text_list = df['Pre-processing']  # switch out with processed text maybe?
    print(len(text_list))

    f = open('to-tag.txt', 'w')

    for i in range(start_num, end_num - 1):
        try:
            f.write('@ \n ')
            text = str(text_list[i].encode('utf-8'))
            t1 = text.replace("\\r", " ")
            t2 = t1.replace("b'", "")
            t3 = t2.replace("\\r\\n", "")
            t4 = t3.replace("\\n", "")
            t5 = t4.replace("\\", " \\")
            f.write(t4)
        except:
            f.write(f"\n \n {i} was not written")
        # f.write("\n \n")
        print("write")

    print("done")
    f.close()


if __name__ == "__main__":
    main()
