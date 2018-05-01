import sys
import logging
import xml.etree.ElementTree
from argparse import ArgumentParser

import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
from openpyxl.styles import Alignment

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger()


def fetch_course_urls():
   xml_sitemap_url = 'https://www.coursera.org/sitemap~www~courses.xml'
   xml_list = requests.get(xml_sitemap_url).text
   urlset = xml.etree.ElementTree.fromstring(xml_list)
   course_urls = [url[0].text for url in urlset]
   return course_urls


def fetch_course_info(course_url):
   html_doc = requests.get(course_url).text
   soup = BeautifulSoup(html_doc, 'html.parser')
   tags = {
       'name': soup.find('h1', class_='title'),
       'languages': soup.find('div', class_='rc-Language'),
       'start_date': soup.find('div', class_='rc-StartDateString'),
       'rating': soup.find('div', class_='ratings-text'),
   }
   course = {}
   for tag_name, tag_content in tags.items():
       course[tag_name] = tag_content.get_text() if tag_content else None
   weeks_tag = soup.find('div', class_='rc-WeekView')
   course['number_of_weeks'] = len(weeks_tag.contents) if weeks_tag else None
   return course


def format_course_info(course_info):
   for tag_name in course_info.keys():
       course_info[tag_name] = course_info[tag_name] or 'N/A'
   return course_info


def output_courses_into_xlsx(courses, filepath):
   if not courses:
       raise ValueError('There must be at least one course to save')
   workbook = Workbook()
   worksheet = workbook.active
   worksheet.title = 'Coursera courses info'
   worksheet.merge_cells('A1:E1')
   worksheet.append([worksheet.title])
   worksheet['A1'].alignment = Alignment(horizontal='center')
   worksheet.append(list(courses[0].keys()))
   for course in courses:
       worksheet.append(list(course.values()))
   workbook.save(filepath)


def parse_args(argv):
   parser = ArgumentParser()
   parser.add_argument('--number_of_courses', '-n', type=int, default=20)
   parser.add_argument('--filepath', '-f', type=str, default='output.xlsx')
   return parser.parse_args(argv)


if __name__ == '__main__':
   args = parse_args(sys.argv[1:])
   logger.info('fetching course urls...')
   course_urls = fetch_course_urls()
   courses = []
   for course_url in course_urls[:args.number_of_courses]:
       logger.info('fetching {0}...'.format(course_url))
       course_info = fetch_course_info(course_url)
       formatted_course_info = format_course_info(course_info)
       courses.append(formatted_course_info)

