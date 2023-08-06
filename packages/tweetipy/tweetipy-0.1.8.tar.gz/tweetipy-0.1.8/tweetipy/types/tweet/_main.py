from typing import Union
from .. import Includes, Attachments, ContextAnnotation
from .metrics import PublicMetrics


class Tweet():
    def __init__(self, id: str, text: str, attachments: Attachments = None, edit_history_tweet_ids: list[str] = None, context_annotations: list[ContextAnnotation] = None, author_id: str = None, public_metrics: PublicMetrics = None, includes: Includes = Includes()): #, API: Tweetipy = None) -> None:
        self._id = id
        self._text = text
        self._attachments = Attachments(**attachments) if attachments != None else None
        self._edit_history_tweet_ids = edit_history_tweet_ids
        self._context_annotations = [ContextAnnotation(**x) for x in context_annotations] if context_annotations != None else None
        self._author_id = author_id
        self._public_metrics = PublicMetrics(**public_metrics) if public_metrics != None else None
        self._includes = includes if isinstance(includes, Includes) else Includes(**includes)
    
    @property
    def id(self):
        return self._id
    
    @property
    def text(self):
        return self._text

    @property
    def attachments(self) -> Union[Attachments, None]:
        return self._attachments

    @property
    def url(self):
        return f'https://twitter.com/account/status/{self.id}'
    
    @property
    def edit_history_tweet_ids(self):
        return self._edit_history_tweet_ids
    
    @property
    def context_annotations(self) -> Union[list[ContextAnnotation], None]:
        return self._context_annotations
    
    @property
    def author_id(self):
        return self._author_id
    
    @property
    def author_handle(self):
        if self.includes != None:
            if self.includes.users != None:
                for user in self.includes.users:
                    if user.id == self.author_id:
                        return user.username
        return None
    
    @property
    def public_metrics(self) -> Union[PublicMetrics, None]:
        return self._public_metrics
    
    @property
    def includes(self) -> Includes:
        return self._includes
    
    def dict(self):
        base_dict = {
            "id": self.id,
            "text": self.text,
            "url": self.url,
            "edit_history_tweet_ids": self.edit_history_tweet_ids,
            "context_annotations": self.context_annotations,
            "author_id": self.author_id,
            "public_metrics": self.public_metrics
        }
        clean_dict = {}
        for key, val in base_dict.items():
            if val != None:
                clean_dict[key] = val
        return clean_dict
    
    def json(self):
        return str(self.dict())

    def __str__(self) -> str:
        tweet_repr = [
            '{s:{c}<{n}}'.format(s=f'# Tweeet ID: {self.id} ', n=70, c='-'),
            f"# URL:  {self.url}",
        ]
        if self.public_metrics != None:
            tweet_repr.append(f"# {str(self.public_metrics)}")
        if self.author_handle != None:
            tweet_repr.append(f"# Author: @{self.author_handle}")
        if self.author_id != None:
            tweet_repr.append(f"# Author ID: {self.author_id}")
            
        if self.context_annotations != None:
            if len(self.context_annotations) > 0:
                tweet_repr.append('# Context annotations:')
                for i in range(len(self.context_annotations)):
                    context = self.context_annotations[i]
                    tweet_repr.append(f'# - [{i}]: {str(context)}')
        
        tweet_repr.append(f"# Text: {self.text}")
        tweet_repr.append("# " + "-"*68 + '\n')
        return '\n'.join(tweet_repr)
    
    def __repr__(self) -> str:
        return str(self.dict())
