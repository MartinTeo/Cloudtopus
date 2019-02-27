from __future__ import absolute_import, unicode_literals
from celery.utils.log import get_task_logger
from celery import shared_task
from Module_TeamManagement.src import utilities
from Module_TeamManagement.src import selenium_using_chrome
from background_task import background

logger = get_task_logger(__name__)

@shared_task(name='trailheadscrapper')
def webscrapper():
    # Saves latest image from Flickr    
    utilities.cloud_learning_tool_logging()
    utilities.webScrapper()
