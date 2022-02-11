#!/usr/bin/env python
#-*-coding:utf-8-*-

import json
import csv
import lxml.etree as ET
import xmltodict
import pandas as pd
import argparse, os

def csvtoxml(val1,val2):
    # Reading csv file and build tree
    f = open(val1)
    csvreader = csv.reader(f, delimiter=';')
    headers = next(csvreader)
    file= open(val2, 'wb')
    file.write("<root>\n")
    for count, row in enumerate(csvreader):

        # Initializing XML
        # Call, Data, audio and ets - your custom fields (if need)
        root = ET.Element("root")
        custom = ET.SubElement(root, "Custom_Data")
        data = ET.SubElement(custom, "Data")
        for column_index, value in enumerate(row):
            column_name = headers[column_index]

            
            ET.SubElement(data, column_name).text = value

        # Dumping XML tree to string
        tree_out = (ET.tostring(data,pretty_print=True,))

        # Writing xml to file
        file.write(tree_out)
    #write
    file.write("</root>")

def xmltocsv(val1,val2):
    file = open(val1,'r')
    str = file.read()
    dictionary = xmltodict.parse(str)
    df = pd.DataFrame(dictionary)
    # Do any parsing of the XML file here, as you'll want to confirm that you are writing the correct info to csv. 
    df.to_csv(val2)

def xmltojson(val1,val2):
    json_filename=val2
    xml_filename=val1
    with open(xml_filename) as xml_file:
        my_dict=xmltodict.parse(xml_file.read())
    xml_file.close()
    json_data=json.dumps(my_dict)


    with open(json_filename, 'w') as outfile:
        json.dump(my_dict,outfile, indent=4, sort_keys=True)


    body = my_dict["h:html"]["h:body"]
    df_body = dict()
    for key in body.keys():
        if type(body[key]) is list:
            df_body[key]=pd.DataFrame.from_dict(body[key])

def jsontoxml(val1,val2):
  import json as j
  with open(val1) as json_format_file: 
    d = j.load(json_format_file)
  import xml.etree.cElementTree as e
  r = e.Element("root")
  data = e.SubElement(r,"Data")

  try:
    for z in d["Data"]:
      e.SubElement(data,"BURS").text = z["BURS"]
      e.SubElement(data,"DIL").text = z["DIL"]
      e.SubElement(data,"FAKULTE").text = z["FAKULTE"]
      e.SubElement(data,"GECEN_YIL_MIN_PUAN").text = z["GECEN_YIL_MIN_PUAN"]
      e.SubElement(data,"GECEN_YIL_MIN_SIRALAMA").text = z["GECEN_YIL_MIN_SIRALAMA"]
      e.SubElement(data,"KONTENJAN").text = z["KONTENJAN"]
      e.SubElement(data,"OGRENIM_SURESI").text = z["OGRENIM_SURESI"]
      e.SubElement(data,"OGRENIM_TURU").text = z["OGRENIM_TURU"]
      e.SubElement(data,"OKUL_BIRINCISI_KONTENJANI").text = z["OKUL_BIRINCISI_KONTENJANI"]
      e.SubElement(data,"PROGRAM").text = z["PROGRAM"]
      e.SubElement(data,"PROGRAM_KODU").text = z["PROGRAM_KODU"]
      e.SubElement(data,"PUAN_TURU").text = z["PUAN_TURU"]
      e.SubElement(data,"UNIVERSITE").text = z["UNIVERSITE"]
      e.SubElement(data,"UNIVERSITE_TURU").text = str(z["UNIVERSITE_TURU"])
    a = e.ElementTree(r)
    a.write("json_to_xml.xml")
    a.write(val2)
    exit()
  except Exception as e:
      # error loading file
    print("Error loading file ... exiting:",e)
    exit()
 
def csvtojson(val1,val2):
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", default=val1, nargs='?', help='Input file name, default: test.csv')
    parser.add_argument("outfile", default='csvtojson.json', nargs='?', help='Output file name, default: [infile_basename].json')
    parser.add_argument('-S', '--separator', default=';', help='CSV separator used, default ";"')
    parser.add_argument('-H', '--headerline', type=int, default=0, help='Header line to use as column names')
    parser.add_argument('-c', '--columns', type=int, help='Number of columns to crop to')
    parser.add_argument('-p', '--printdata', action='store_true', help='Print formatted data when done')

    args = parser.parse_args()

    infile = args.infile
    if not os.path.isfile(infile):
        print('File "%s" does not exist, aborting. Use --help to show command syntax and command line options.' % infile)
        exit()

    outfile = args.outfile
    if outfile is None:
        outfile = os.path.splitext(infile)[0] + '.json'

    print("Converting %s -> %s [sep=%s, header=%s]" %
        (infile, outfile, args.separator, args.headerline))


    import pandas as pd

    try:
        df = pd.read_csv(
            infile, sep=args.separator, header=args.headerline,
            engine='python'
        )
    except Exception:
        print('Could not read CSV data from "%s":\n' % infile)
        raise

    # crop columns
    if args.columns:
        df = df[df.columns[:args.columns]]

    # remove empty rows
    df.dropna(how='all')

    df.to_json(outfile, orient='records')

    if args.printdata:
        print(df)

def jsontocsv(val1,val2):
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", default=val1, nargs='?', help='Input file name, default: test.json')
    parser.add_argument("outfile", default='jsontocsv.csv', nargs='?', help='Output file name, default: [infile_basename].csv')
    parser.add_argument('-S', '--separator', default=';', help='CSV separator used, default ","')
    parser.add_argument('-i', '--index', action='store_true', help='Write row names (index)')
    parser.add_argument('-I', '--indexlabel', help='Label for index column')
    parser.add_argument('-u', '--usecols', nargs='+', help='List of names of columns to use')
    parser.add_argument('-p', '--printdata', action='store_true', help='Print formatted data when done')

    args = parser.parse_args()

    infile = args.infile
    if not os.path.isfile(infile):
        print('File "%s" does not exist, aborting. Use --help to show command syntax and command line options.' % infile)
        exit()

    outfile = args.outfile
    if outfile is None:
        outfile = os.path.splitext(infile)[0] + '.csv'

    print("Converting %s -> %s [sep=%s]" %
        (infile, outfile, args.separator))
    if args.usecols is not None:
        print("Only using columns: %s" % (' '.join(args.usecols),))


    import pandas as pd
    try:
        df = pd.read_json(infile)
    except ValueError:
        print('Could not read JSON data from "%s":\n' % infile)
        raise


    # Convert
    if args.usecols is None:
        df.to_csv(outfile, index=args.index, index_label=args.indexlabel, sep=args.separator)
    else:
        df.to_csv(outfile, index=args.index, index_label=args.indexlabel, sep=args.separator, columns=args.usecols)

    if args.printdata:
        print(df)

def validate(val1,val2):
    from lxml import etree
    from io import StringIO

    doc = etree.parse(val1)
    root = doc.getroot()
    #print(etree.tostring(root))
    xmlschema_doc = etree.parse('test.xsd')
    xmlschema = etree.XMLSchema(xmlschema_doc)
    doc = etree.XML(etree.tostring(root))
    validation_result = xmlschema.validate(doc)
    print(validation_result)
    xmlschema.assert_(doc)

def main():
   
    while True:
      try:
         print("python 2014510056.py <inputfile> <outputfile> <type>\n")
          #print("python 2014510056.py ")
         val1=input("inputfile ")
         val2=input("outputfile ")
         val3=int(input("type "))
         if val3==1:
            csvtoxml(val1,val2)
         elif val3==2:
            xmltocsv(val1,val2)
         elif val3==3:
            xmltojson(val1,val2) 
         elif val3==4:
            jsontoxml(val1,val2)
         elif val3==5:
            csvtojson(val1,val2)
         elif val3==6:
            jsontocsv(val1,val2)
         elif val3==7:
            validate(val1,val2)
         else:
             print("wrong type")            
      except ValueError:
         print("")
         continue
main()