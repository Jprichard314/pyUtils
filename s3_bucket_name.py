from dataclasses import dataclass, field
from urllib.parse import urlencode
from datetime import datetime

@dataclass
class s3_bucket_object:

    key: str = field(init = False)
    project: str
    tags: dict
    stage: str
    encoded_tags: str = field(init=False)
    datetime_partitions: str = field(init=False)

    # Defined required tags
    required_tags = {
            "retention":["3_months","6_months","12_months"],
            "source":[],
            "description":[]
        }
    
    # Set bucket stage
    # for right now, we'll error if anything other
    # than raw is passed because we don't have
    # partitioning enabled for them.
    valid_stages = ["raw"]
    
    def __post_init__(self):

        # validate tag input
        for key in self.required_tags.keys():
            if key not in self.tags.keys():
                raise ValueError(f"Missing required tag: {key}")
            if len(self.required_tags[key]) == 0:
                pass
            else:
                if self.tags[key] not in self.required_tags[key]:
                    raise ValueError(f"Tag '{key}' set with improper value. \n Accepted values {self.required_tags[key]}")

        self._encode_tags()
        self._create_datetime_partitions()
        self._create_key()
            
    
    def _encode_tags(self):
        """
            boto's S3 put_object method required url encoded tags
            and this facilitates that
        """
        self.encoded_tags = urlencode(self.tags)

    def _create_datetime_partitions(self):
        if self.stage == 'raw':
            self.datetime_partitions = f"{datetime.today():year=%Y/month=%m/day=%d}"
        else:
            pass
    
    def _create_key(self):
        self.key = f"{self.project}/{self.datetime_partitions}/data.parquet"


    def push_to_bucket(self):
        pass
    


    # write to bucket