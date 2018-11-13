import csv
import sys, getopt
import pandas as pd
""" This script reads the header.csv file to get all column start and end positions as well as column headers.
It then opens the data file and parses it line by line to create a formatted comma separated value. """

def main( argv ):
    #declare variables
    colPos = []
    header = ""
    headerKey = ""
    fname = ""
    oname = ""
    sheet = ""
    try:
        opts, args = getopt.getopt( argv,"hi:s:k:", [ "ifile=", "sheet=", "kfile=" ] )
    except getopt.GetoptError:
        print ( 'parseCDC.py -i <inputFile> -s <sheet> -k <headerKeyFile>' )
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ( 'parseCDC.py -i <inputFile> -s <sheet> -k <headerKeyFile>' )
        elif opt in ( "-i", "--ifile" ):
            fname = arg
            oname = arg + '.csv'
        elif opt in ( "-s", "--sheet" ):
            sheet = arg
        elif opt in ( "-k", "--kfile" ):
            headerKey = arg
    if fname != "" and sheet != "" and headerKey != "":
        #use pandas to read Excel file
        xls = pd.ExcelFile( headerKey )
        sheet1 = xls.parse( sheet )
        for index, row in sheet1.iterrows():
            """ create a tuple pair of beginning and end position of columns
            since it's zero based we subtract 1 from the beginning position
            since the last number represents where to stop we do NOT substract one from the end position
            we also need to cast the str variables as int """
            colSpacing = ( int(row[0]) - 1, int(row[1]))
            #append tuple pair to colSpacing list
            colPos.append(colSpacing)

            #append all header entries to header string
            header += row[3].strip() + ","
        #remove trailing comma from header string
        header = header[:-1]

        #open file to write to
        with open( oname, "w" ) as output:
            #write header string to first line
            output.write( header + "\n" )
            #loop through data file
            with open( fname ) as f:
                #for each row get data for each column and append to line
                for row in f:
                    line = ""
                    #loop through tuple pairs to get position of each column
                    for col in colPos:
                        #append column data to line
                        line += row[col[0]:col[1]].strip() + ","
                    #remove trailing comma
                    line = line[:-1]
                    #write line to output file
                    output.write( line + "\n" )
    else:
        print ( 'Be sure all parameters are met' )
        print ( 'parseCDC.py -i <inputFile> -o <outputFile> -k <headerKeyFile' )
            

if __name__ == "__main__":
   main(sys.argv[1:])