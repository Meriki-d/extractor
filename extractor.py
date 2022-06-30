#necessary imports
import pdfplumber as pp
from hscode import hstable
from datetime import datetime as dt
# from converterapi import convert_to_ksh

import re

filepath=''

def read_pdf_content(filepath):
    #read pdf
    try:
        pdf_file =pp.open(rf'{filepath}')

        allcontent=[]
        pages=pdf_file.pages

        allcontent=[]

        for page in pages:
            pagedata=page.extract_text()
            allcontent.append(pagedata)

        allcontent = [item for sublist in allcontent for item in sublist]
        print(allcontent)
        return allcontent
    except:
        print('error reading data')
        return


def correct_invoice_checker(allcontent):
    try:
        # write regex code for identify if correct invoice or not
        # link to regex tutorial https://www.w3schools.com/python/python_regex.asp
        pass
    except:
        print('Invalid invoice')
        return False


postdata={

}

# r_type (correct invoice or not) is true or false 
def simplified_items_(items,r_type=None):
    
    try:
        simplified_items=[]
        
        
        # regex for finding amounts
        
        # common example in most invoices

        for i in items:
            try:
                res=(bool(re.search(r'\bKES[+-]?([0-9]*[.])?[0-9]+', i).group(0)))
            except AttributeError:
                res=(bool(re.search(r'\bKES[+-]?([0-9]*[.])?[0-9]+', i)))
            
        if res==True:
            itemholder=i.split()
            simplified_items.append(itemholder)
        return simplified_items
    except:
        print('error simplifying items')
        return []

# identify the endpoint of required data. --- write a regex for that based on different receipt
def basicdata(allcontent,endingpoint,return_number=None,
        invoice_no=None,
        credit_no=None):
    try:
        
        invoice_no=allcontent.split(' ')[-1]
        pin_no=line.split(' ').split('/').upper()
        print('pin number found')
            
            
        taxableamtline=endingpoint
        taxline=endingpoint+2
        totalamtline=taxline+2

        # print('about to process the amounts')
        taxableamt=round(float(allcontent[taxableamtline].strip().replace(",","")),2)
        tax=round(float(allcontent[taxline].strip().replace(",","")),2)
        totalamt=round(float(allcontent[totalamtline].strip().replace(",","")),2)
        print('able to process')
        print('total amt = ',totalamt)
        print('tax amt = ',tax)
        print('taxable amt = ',taxableamt)
        # print("we are at currency conversion")
                    #########################   CALL API FOR CURRENCY CONVERSION HERE ####
        
        for indx,line in enumerate(allcontent):
            pline=indx+1
            break
        pin_no,invoice_no=allcontent[pline].split().upper()
        
       
        # print("addng rest of basic data")
        postdata["SenderId"]="d13b89eca2a89a5b22ee" 
        #invoice timestamp
        time=dt.now().replace(microsecond=0).isoformat()
        postdata['InvoiceTimeStamp']=time
        #invoice category
        #invoice number assigned by our machine
        if invoice_no:
            # print("checking invoice no")
            postdata["InvoiceCategory"]='Tax Invoice'
            postdata["TraderSystemInvoiceNumber"]=invoice_no
            # print('working upto here==>invoice no',invoice_no)
            return_number=invoice_no
        elif credit_no:
            # print("checking credit no")
            postdata["InvoiceCategory"]='Credit Note'
            postdata["TraderSystemInvoiceNumber"]=credit_no
            return_number=credit_no
            
        else:
            postdata["InvoiceCategory"]='Debit Invoice'
            postdata["TraderSystemInvoiceNumber"]=0
        #relevant invoice number only for credit note
        postdata['RelevantInvoiceNumber']=''

        postdata['PINOfBuyer']=pin_no

            #discount
        discount=0
        postdata['InvoiceType']='Original'
        postdata['Discount']=discount
        # total invoice amount
        postdata['TotalInvoiceAmount']=totalamt
        #total taxable amount
        postdata['TotalTaxableAmount']=taxableamt
        # total tax amount
        postdata['TotalTaxAmount']=tax
        # exemtion number no vat
        ExemptionNumber=''
        postdata['ExemptionNumber']=ExemptionNumber
        return postdata
    
    except:
        with open('logfile','w') as f:
            f.write('error getting b data')
        return None,None,None


def generate_hscodes(itemname):
    try:
        if itemname in hstable.keys():
            hsdesc,pc=[(i,v) for i,v in itemname.values()]
            return hsdesc,pc
        
    except:
        with open('logfile','w') as f:
            f.write('hscode retrieval error')

    return

def get_individual():
    try:
        dct={}
        i=[]
        
        hsdesc=' '
        amt=round(float(i[-1].strip().replace(",","")),2)
        tax=round(float(i[-2].strip().replace(",","")),2)
        unit=round(float(i[-3].strip().replace(",","")),2)
        num=int(float(i[-4].replace(",","")))
        
        hscode,pc=generate_hscodes(hsdesc)
        if int(tax) == 0:
            pc=0
        # tax=round(unit*(pc/100),2)
        transactiontype='1'
        dct['HSDesc']=hsdesc
        dct['TaxRate']=pc
        dct['ItemAmount']=amt
        dct['TaxAmount']=tax
        dct['TransactionType']=transactiontype
        dct['UnitPrice']=unit
        dct['HSCode']=hscode
        dct['Quantity']=num
        dct={}

        postdata['ItemDetails']=dct
        return
    except:
        print('error in getting individual details')
        return

finalpost={}
finalpost['Invoice']=postdata




if __name__=='__main__':
    allcontent=read_pdf_content()
    correct_invoice_checker(allcontent)
    items=simplified_items_(allcontent)
    generate_hscodes(items)
    get_individual()
    print(finalpost) #====== this returns the postdata for kra api