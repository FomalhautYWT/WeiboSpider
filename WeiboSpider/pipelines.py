# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import psycopg2, logging
from psycopg2 import errorcodes
from .items import UserInfoItem, FollowItem, FanItem, \
    PostInfoItem, TextItem, ImageItem, CommentItem, ForwardItem, ThumbupItem



# TODO 添加建立表的功能。
class WeibospiderPipeline(object):
    def __init__(self, username, database):
        self.username = username
        self.database = database

        self.user_info_item_count = 1
        self.follow_item_count = 1
        self.fan_item_count = 1
        self.post_info_item_count = 1
        self.text_item_count = 1
        self.image_item_count = 1
        self.comment_item_count = 1
        self.forward_item_count = 1
        self.thumbup_item_count = 1

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            username = crawler.settings.get('POSTGRESQL_USERNAME'),
            database = crawler.settings.get('POSTGRESQL_DATABASE')
        )

    def open_spider(self, spider):
        try:
            self.connector = psycopg2.connect(
                user = self.username,
                database = self.database
            )
            self.cursor = self.connector.cursor()
            self.logger.info('Conneting to database successfully!')
        except psycopg2.Error as e:
            self.logger.error(
                'Failed to connect database. Returned: %s'
                  % errorcodes.lookup(e.pgcode)
            )
            exit(-1)

    def close_spider(self, spider):
        self.cursor.close()
        self.connector.close()

    def process_item(self, item, spider):
        if isinstance(item, UserInfoItem):
            try:
                self.cursor.execute(
                    '''INSERT INTO user_info (user_id, user_name, gender, district)
                        VALUES (%(user_id)s, %(user_name)s, %(gender)s, %(district)s);''',
                    dict(item)
                )
                self.connector.commit()
                self.logger.info('Write a user_info item into database. Seq: {0:d}'.format(self.user_info_item_count))
                self.user_info_item_count += 1
            except psycopg2.Error as e:
                self.logger.error(
                    "Failed to insert data into user_info table. Returned: %s"
                      % errorcodes.lookup(e.pgcode)
                )
        elif isinstance(item, FollowItem):
            try:
                self.cursor.execute(
                    '''INSERT INTO follow (user_id, follow_list)
                        VALUES (%(user_id)s, %(follow_list)s);''',
                    dict(item)
                )
                self.connector.commit()
                self.logger.info('Write a follow item into database. Seq: {0:d}'.format(self.follow_item_count))
                self.follow_item_count += 1
            except psycopg2.Error as e:
                self.logger.error(
                    "Failed to insert data into follow table. Returned: %s"
                      % (errorcodes.lookup(e.pgcode))
                )
        elif isinstance(item, FanItem):
            try:
                self.cursor.execute(
                    '''INSERT INTO fan (user_id, fan_list)
                        VALUES (%(user_id)s, %(fan_list)s);''',
                    dict(item)
                )
                self.connector.commit()
                self.logger.info('Write a fan item into database. Seq: {0:d}'.format(self.fan_item_count))
                self.fan_item_count += 1
            except psycopg2.Error as e:
                self.logger.error(
                    "Failed to insert data into fan table. Returned: %s"
                      % (errorcodes.lookup(e.pgcode))
                )
        elif isinstance(item, PostInfoItem):
            try:
                self.cursor.execute(
                    '''INSERT INTO post_info (user_id, post_id, publish_time)
                        VALUES (%(user_id)s, %(post_id)s, %(publish_time)s);''',
                    dict(item)
                )
                self.connector.commit()
                self.logger.info('Write a post_info item into database. Seq: {0:d}'.format(self.post_info_item_count))
                self.post_info_item_count += 1
            except psycopg2.Error as e:
                self.logger.error(
                    "Failed to insert data into follow table. Returned: %s"
                      % (errorcodes.lookup(e.pgcode))
                )
        elif isinstance(item, TextItem):
            try:
                self.cursor.execute(
                    '''INSERT INTO text (user_id, post_id, text)
                        VALUES (%(user_id)s, %(post_id)s, %(text)s);''',
                    dict(item)
                )
                self.connector.commit()
                self.logger.info('Write a text item into database. Seq: {0:d}'.format(self.text_item_count))
                self.text_item_count += 1
            except psycopg2.Error as e:
                self.logger.error(
                    "Failed to insert data into text table. Returned: %s"
                      % (errorcodes.lookup(e.pgcode))
                )
        elif isinstance(item, ImageItem):
            try:
                self.cursor.execute(
                    '''INSERT INTO image (user_id, post_id, image_list)
                        VALUES (%(user_id)s, %(post_id)s, %(image_list)s);''',
                    dict(item)
                )
                self.connector.commit()
                self.logger.info('Write an image item into database. Seq: {0:d}'.format(self.image_item_count))
                self.image_item_count += 1
            except psycopg2.Error as e:
                self.logger.error(
                    "Failed to insert data into image table. Returned: %s"
                      % (errorcodes.lookup(e.pgcode))
                )
        elif isinstance(item, CommentItem):
            try:
                self.cursor.execute(
                    '''INSERT INTO comment (user_id, post_id, comment_list)
                        VALUES (%(user_id)s, %(post_id)s, %(comment_list)s::json[]);''',
                    dict(item)
                )
                self.connector.commit()
                self.logger.info('Write a comment item into database. Seq: {0:d}'.format(self.comment_item_count))
                self.comment_item_count += 1
            except psycopg2.Error as e:
                self.logger.error(
                    "Failed to insert data into comment table. Returned: %s"
                    % (errorcodes.lookup(e.pgcode))
                )
        elif isinstance(item, ForwardItem):
            try:
                self.cursor.execute(
                    '''INSERT INTO forward (user_id, post_id, forward_list)
                        VALUES (%(user_id)s, %(post_id)s, %(forward_list)s::json[]);''',
                    dict(item)
                )
                self.connector.commit()
                self.logger.info('Write a forward item into database. Seq: {0:d}'.format(self.forward_item_count))
                self.forward_item_count += 1
            except psycopg2.Error as e:
                self.logger.error(
                    "Failed to insert data into forward table. Returned: %s"
                    % (errorcodes.lookup(e.pgcode))
                )
        elif isinstance(item, ThumbupItem):
            try:
                self.cursor.execute(
                    '''INSERT INTO thumbup (user_id, post_id, thumbup_list)
                        VALUES (%(user_id)s, %(post_id)s, %(thumbup_list)s::json[]);''',
                    dict(item)
                )
                self.connector.commit()
                self.logger.info('Write a thumb-up item into database. Seq: {0:d}'.format(self.thumbup_item_count))
                self.thumbup_item_count += 1
            except psycopg2.Error as e:
                self.logger.error(
                    "Failed to insert data into thumbup table. Returned: %s"
                    % (errorcodes.lookup(e.pgcode))
                )

        return item
