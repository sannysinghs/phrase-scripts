#!/usr/bin/env python

#  Copyright (c) 2012-2020 Grab Taxi Holdings PTE LTD (GRAB), All Rights Reserved. NOTICE: All information contained herein is, and remains the property of GRAB. The intellectual and technical concepts contained herein are confidential, proprietary and controlled by GRAB and may be covered by patents, patents in process, and are protected by trade secret or copyright law.
#  You are strictly forbidden to copy, download, store (in any medium), transmit, disseminate, adapt or change this material in any way unless prior written permission is obtained from GRAB. Access to the source code contained herein is hereby forbidden to anyone except current GRAB employees or contractors with binding Confidentiality and Non-disclosure agreements explicitly covering such access.
#
#  The copyright notice above does not evidence any actual or intended publication or disclosure of this source code, which includes information that is confidential and/or proprietary, and is a trade secret, of GRAB.
#  ANY REPRODUCTION, MODIFICATION, DISTRIBUTION, PUBLIC PERFORMANCE, OR PUBLIC DISPLAY OF OR THROUGH USE OF THIS SOURCE CODE WITHOUT THE EXPRESS WRITTEN CONSENT OF GRAB IS STRICTLY PROHIBITED, AND IN VIOLATION OF APPLICABLE LAWS AND INTERNATIONAL TREATIES. THE RECEIPT OR POSSESSION OF THIS SOURCE CODE AND/OR RELATED INFORMATION DOES NOT CONVEY OR IMPLY ANY RIGHTS TO REPRODUCE, DISCLOSE OR DISTRIBUTE ITS CONTENTS, OR TO MANUFACTURE, USE, OR SELL ANYTHING THAT IT MAY DESCRIBE, IN WHOLE OR IN PART.

#
import glob
import os
import subprocess
import yaml
from argparse import ArgumentParser

project_path = '/Users/sanny.segue/Documents/pax/pax-android/'

# file_path, tag
def generate_phrase_app_yml(files):
  
  read_access_token = '2f633240b0b64b68b63e6b942b80b7b60187a39ef49cd9f8e5fefe432760ef28'
  access_token = os.environ.get('PHRASEAPP_ACCESS_TOKEN', read_access_token)

  project_id = '19eb11bb0280a5334693247c74b02431'
  locale_id = 'd2848c5f3c3ea06f15d3ba89e6bc4549'
  file_format = "xml"

  sources, targets = [], []

  for file in files:
    tag = file['tag']
    file_path = file['path']

    sources.append({
      'file': file_path,
      'params': {
        'locale_id': locale_id,
        'tags': tag,
        'update_translations': False,
        'skip_upload_tags': True
      }
    })

    targets.append({
      'file': file_path,
        'params': {
          'tag': tag,
          'locale_id': locale_id,
          'encoding': 'UTF-8',
          'format_options': {
            'enclose_in_cdata': True,
            'convert_placeholder': True
          }
        }
    })

  data = {
    'phraseapp': {
      'access_token': access_token,
      'file_format': file_format,
      'project_id': project_id,
      'pull': {
        'targets': targets
      },
      'push': {
        'sources': sources
      }
    }
  }

  print("generate")
  phrase_ouput_file = '{}.phraseapp.yml'.format(project_path)
  print(phrase_ouput_file)
  # write to .phraseapp.yml file
  with open(phrase_ouput_file, 'w') as outfile:
    yaml.dump(data, outfile, default_flow_style=False)