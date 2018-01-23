# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import xlsxwriter

class FirstscrapyprjPipeline(object):
    def process_item(self, item, spider):
        return item


class XlsxWriterPipeline(object):    

    def open_spider(self, spider):
        #self.file = open('output.xlsx', 'w')
        # Create an new Excel file and add a worksheet.
        self.tekstr=1
        self.workbook = xlsxwriter.Workbook('output.xlsx')
        self.worksheet = self.workbook.add_worksheet("Выгрузка")
        fields = ['author','text_quote','tags']
        i=0
        for i in range(0,len(fields)):
            self.worksheet.write(0,i, fields[i])            
        self.worksheet.set_column(0,len(fields), 30)
        bold = self.workbook.add_format({'bold': True})

    def close_spider(self, spider):
        self.tekstr=0
        self.workbook.close()

    def process_item(self, item, spider):
        print("Элементы = = = ",item)
        self.worksheet.write(self.tekstr,0, item["author"][0])
        self.worksheet.write(self.tekstr,1, item["text_quote"][0])
        self.worksheet.write(self.tekstr,2, str(item["tags"]))
        self.tekstr = self.tekstr + 1
        return item