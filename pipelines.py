# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
from scrapy.exporters import CsvItemExporter
from TechSiteScrapper.items import ContentItem, HistoryItem
from scrapy.utils.project import get_project_settings

class TechsitescrapperPipeline(object):
    settings = get_project_settings()
    HISTORY_FILE_NAME = settings.get('HISTORY_FILENAME', "Crawled History.csv")
    CONTENT_FILE_NAME = settings.get('CONTENT_FILENAME', "Crawled Content.csv")
    HISTORY_ITEM_SIZE = 100
    CONTENT_ITEM_SIZE = 100
    history_items = []
    content_items = []
    history_item_counter = {'gotten' : 0, 'dumpped' : 0}
    content_item_counter = {'gotten' : 0, 'dumpped' : 0}


    # Method called when spider started running
    def open_spider(self, spider):
        currentPath = os.path.dirname(__file__)
        self.HISTORY_FILE_PATH = os.path.join(currentPath, "files/" + self.HISTORY_FILE_NAME)
        self.CONTENT_FILE_PATH = os.path.join(currentPath, "files/" + self.CONTENT_FILE_NAME)

    # Method called when spider finished
    def close_spider(self, spider):
        self.dump_crawled_links_to_file()
        self.dump_crawled_content_to_file()
        print("[CLOSING] Closing Item Pipeline")
        print(
            "[RESULT] History Item - Gotten: {} ; Dumpped: {}".format( 
            self.history_item_counter['gotten'], self.history_item_counter['dumpped']
            ))
        print(
            "[RESULT] Content Item - Gotten: {} ; Dumpped: {}".format(
            self.content_item_counter['gotten'], self.content_item_counter['dumpped']
        )) 
 
       

    # Process the items crawled by the spider
    def process_item(self, item, spider):

        if isinstance(item, ContentItem):
            print("[ITEM] Got Content Item! ")
            self.content_item_counter["gotten"] += 1

            # Clean the contents got from forum
            item['content'] = self.clean_content(item['content'])
            self.content_items.append(item)
            if len(self.content_items) > self.CONTENT_ITEM_SIZE:
                self.dump_crawled_content_to_file()
             
        elif isinstance(item, HistoryItem):
            print("[ITEM] Got History Item! ")
            self.history_item_counter["gotten"] += 1

            # Add the item to an array to export it later
            self.history_items.append(item)
            # if there are more than a certian number of item in history item, save them to file
            # to avoid having too much links in the RAM for larger crawl
            if len(self.history_items) > self.HISTORY_ITEM_SIZE:
                self.dump_crawled_links_to_file()
            
        else:
            print("[!!ITEM!!] Ewww, Got WEIRD Item: " + str(item))

        return item

    def dump_crawled_links_to_file(self):

        if self.history_items:
            print("[DUMPING - History Item] Total item count:" + str(len(self.history_items)))
            self.history_item_counter['dumpped'] += len(self.history_items)

            # Check whether does file exist or not
            if os.path.exists(self.HISTORY_FILE_PATH):
                # Open the History File as append
                history_file = open(self.HISTORY_FILE_PATH, "ab")
                # DO NOT print the header for the csv file
                exporter = CustomCsvExporter(history_file, include_headers_line=False)
            else:
                history_file = open(self.HISTORY_FILE_PATH, "wb+")
                exporter = CustomCsvExporter(history_file)
           
            exporter.fields_to_export = ["title", "link"]
            exporter.start_exporting()

            # Export everything in the history items
            for item in self.history_items:
                exporter.export_item(item)

            # Close the exporter and clear the history item
            exporter.finish_exporting()
            history_file.close()
            self.history_items.clear()

    def clean_content(self, contents): 
        tokens = []
        new_content = []
        ditry_contents = ["\n", " "]

        for content in contents:
            tokens = content.split()

            for token in tokens:
                if token not in ditry_contents:
                    new_content.append(token)
                    
        new_content = str(" ").join(new_content)
        return new_content

    def dump_crawled_content_to_file(self):

        if self.content_items:
            print("[DUMPING - Content Item] Total item count:" + str(len(self.content_items)))
            self.content_item_counter['dumpped'] += len(self.content_items)

            # Check whether does file exist or not
            if os.path.exists(self.CONTENT_FILE_PATH):
                # Open the History File as append
                content_file = open(self.CONTENT_FILE_PATH, "ab")
                # DO NOT print the header for the csv file
                exporter = CustomCsvExporter(content_file, include_headers_line=False)
            else:
                content_file = open(self.CONTENT_FILE_PATH, "wb+")
                exporter = CustomCsvExporter(content_file)
           
            exporter.fields_to_export = ["forum_title", "main_category", "sub_category", "link", "content"]
            exporter.start_exporting()

            # Export everything in the history items
            for item in self.content_items:
                exporter.export_item(item)

            # Close the exporter and clear the history item
            exporter.finish_exporting()
            content_file.close()
            self.content_items.clear()
  

class CustomCsvExporter(CsvItemExporter):

    def __init__(self, *args, **kwargs):
        # Get the desired delimiter type from the settings.py named - CSV_DELIMITER
        settings = get_project_settings()
        delimiter = settings.get('CSV_DELIMITER', ',')
        kwargs['delimiter'] = delimiter

        fields_to_export = settings.get('CSV_FIELDS_TO_EXPORT', [])
        if fields_to_export:
            kwargs['fields_to_export'] = fields_to_export

        super(CustomCsvExporter, self).__init__(*args, **kwargs)


    # def dumpToFileJson(self, filename, data, appendFile=False):
    #     # Dump dictionary to a json file
    #     dirname = os.path.dirname(__file__)
    #     filename = os.path.join(dirname, '../links/'+ filename +".json")

    #     if appendFile:
    #         with open(filename, 'a+') as json_file:
    #             json.dump(data, json_file)
    #     else:
    #         with open(filename, 'w+') as json_file:
    #             json.dump(data, json_file)