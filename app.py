#!/usr/bin/python
# -*- coding: utf-8 -*-
#    Copyright 2014 J. Fernando Sánchez Rada - Grupo de Sistemas Inteligentes
#                                                       DIT, UPM
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
'''
Example flask application that uses the EUROSENTIMENT Sentiment Analysis
services to analyse posts from reddit.
'''
from flask import Flask, render_template, request
import clients
import config
import json
import praw
from clients import ServiceClient

app = Flask(__name__)
user_agent = "Test of the EUROSENTIMENT services"

class LazyEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return json.JSONEncoder.default(self, obj)
        except TypeError:
            try:
                return json.JSONEncoder.default(self, vars(obj))
            except TypeError:
                return "**not serializable**"

@app.route('/')
@app.route('/r/<subreddit>')
def home(subreddit="python"):
    r = praw.Reddit(user_agent=user_agent)
    subreddit = r.get_subreddit(subreddit)
    submissions = subreddit.get_top(limit=10)
    return render_template("posts.html", submissions=submissions)

@app.route('/submission/<submission_id>')
def submission(submission_id):
    r = praw.Reddit(user_agent=user_agent)
    s = ServiceClient(config.TOKEN, config.ENDPOINT)
    submission = r.get_submission(submission_id=submission_id,
                                  comment_sort="top")
    comments = praw.helpers.flatten_tree(submission.comments)
    comments = sorted(comments, reverse=True, key=lambda x: x.score)[0:20]
    for comment in comments:
        res = s.request(input=comment.body,
                        intype="direct",
                        informat="text",
                        outformat="json-ld")
        print res
        comment.results = res
        comment.polarity = 0
        num = 0
        for entry in res["entries"]:
            for opinion in entry["opinions"]:
                print "Polarity: %s" % comment.polarity
                num+=1
                comment.polarity+=opinion["marl:polarityValue"]
        comment.polarity = comment.polarity / num
    return render_template('comments.html', comments=comments)


    #return render_template("comments.html", comments=comments)

@app.route('/subreddit')
def subreddit():
    r = praw.Reddit(user_agent=user_agent)
    subreddit = r.get_subreddit('learnpython')
    submissions = subreddit.get_top(limit=10)
    return json.dumps([vars(sub) for sub in submissions], cls=LazyEncoder)

if __name__ == '__main__':
    app.debug = True
    app.run()
