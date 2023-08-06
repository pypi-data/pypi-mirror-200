from datetime import datetime

from lake_loader.base.parser import BaseParser


class TelegramParser(BaseParser):

    def __init__(self):
        pass

    def _get_webpage_photo(self, media):
        if media is None:
            return

        obj = {
            "id": media['id'],
            "date": media['date'],
        }
        return obj

    def _get_media(self, media):
        if media is None:
            return

        if media["_"] == "MessageMediaPhoto":
            media = media['photo']
            obj = {
                "cls": "MessageMediaPhoto",
                "id": media['id'],
                "date": media['date']
            }
        elif media["_"] == "MessageMediaWebPage":
            media = media['webpage']  # get webpage
            obj = {
                "cls": 'MessageMediaWebPage',
                "id": media['id'],
                "url": media['url'],
                "display_url": media['display_url'],
                "type": media['type'],
                "photo": self._get_webpage_photo(media.get("photo", None)),
                "author": media['author'],
                "site_name": media['site_name'],
                "title": media['title'],
                "description": media['description'],
            }
        elif media["_"] == "MessageMediaDocument":
            media = media['document']
            obj = {
                "cls": "MessageMediaDocument",
                "id": media['id'],
                "date": media['date'],
                "mime_type": media.get("mime_type", None),
                "size": media['size']
            }
        else:
            raise NotImplementedError()

        return obj

    def _get_reactions(self, reactions):
        if reactions is None or 'results' not in reactions:
            return

        results = reactions['results']
        rets = []
        for result in results:
            tp = {'reaction': result['reaction'], 'count': result['count']}
            rets.append(tp)
        return rets

    def _get_urls(self, entities):
        if entities is None:
            return

        urls = set([entity['url'] for entity in entities if 'url' in entity])
        return list(urls)

    def _get_replies(self, replies):
        if replies is None:
            return
        return replies['replies']

    def _get_reply_to(self, reply_to):
        if reply_to is None:
            return
        obj = {
            "reply_to_msg_id": reply_to['reply_to_msg_id'],
            "reply_to_scheduled": reply_to["reply_to_scheduled"],
            "reply_to_peer_id": reply_to["reply_to_peer_id"],
            "reply_to_top_id": reply_to["reply_to_top_id"],
        }
        return obj

    def _get_fwd_from(self, fwd_from):
        if fwd_from is None:
            return

        obj = {
            "date": fwd_from['date'],
            "from_id": fwd_from.get("from_id", {}).get("channel_id"),
            "from_name": fwd_from["from_name"],
            "post_author": fwd_from["post_author"]
        }

        return obj

    def parse_data(self, raw_jobj):
        date = datetime.strptime(raw_jobj['date'][:10], '%Y-%m-%d')
        jobj = {
            "id": raw_jobj['id'],
            "channel_id": raw_jobj['peer_id']['channel_id'],
            "date": raw_jobj['date'],
            "date_year": date.year,
            "date_month": date.month,
            "message": raw_jobj['message'],
            "from_id": raw_jobj["from_id"],
            "fwd_from": self._get_fwd_from(raw_jobj.get("fwd_from")),
            "via_bot_id": raw_jobj["via_bot_id"],
            "reply_to": self._get_reply_to(raw_jobj.get("reply_to")),
            "media": self._get_media(raw_jobj.get('media', None)),
            "views": raw_jobj["views"],
            "forwards": raw_jobj["forwards"],
            "replies": self._get_replies(raw_jobj.get('replies', None)),
            "edit_date": raw_jobj["edit_date"],
            "post_author": raw_jobj["post_author"],
            "grouped_id": raw_jobj["grouped_id"],
            "reactions": self._get_reactions(raw_jobj.get('reactions', None)),
            "urls": self._get_urls(raw_jobj.get('entities', None)),
        }
        return jobj
