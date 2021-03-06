import webapp2
import jinja2
import os
from google.appengine.ext import ndb
from google.appengine.ext import db

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class HomepageHandler(webapp2.RequestHandler):
    def get(self):
        home_template = jinja_env.get_template('templates/homepage.html')
        self.response.write(home_template.render())

class AboutUsHandler(webapp2.RequestHandler):
    def get(self):
        about_template = jinja_env.get_template('templates/about_us.html')
        self.response.write(about_template.render())

class ContactUsHandler(webapp2.RequestHandler):
    def get(self):
        contact_template = jinja_env.get_template('templates/contact_us.html')
        self.response.write(contact_template.render())

class SellingHandler(webapp2.RequestHandler):
    def get(self):
        proceed = "Selling"
        posts = NewPost.query().filter(NewPost.category == proceed).fetch()

        list_dict = {
        "num_of_items": len(posts),
        "items": posts
        }
        sell_template = jinja_env.get_template('templates/selling.html')
        self.response.write(sell_template.render(list_dict))

class DonateHandler(webapp2.RequestHandler):
    def get(self):
        proceed = "Donating"
        posts = NewPost.query().filter(NewPost.category == proceed).fetch()

        list_dict = {
        "num_of_items": len(posts),
        "items": posts
        }
        donate_template = jinja_env.get_template('templates/donating.html')
        self.response.write(donate_template.render(list_dict))

class FreelanceHandler(webapp2.RequestHandler):
    def get(self):
        proceed = "Freelance"
        posts = NewPost.query().filter(NewPost.category == proceed).fetch()

        list_dict = {
        "num_of_items": len(posts),
        "items": posts
        }
        free_template = jinja_env.get_template('templates/freelance.html')
        self.response.write(free_template.render(list_dict))

class TradingHandler(webapp2.RequestHandler):
    def get(self):
        proceed = "Trading"
        posts = NewPost.query().filter(NewPost.category == proceed).fetch()

        list_dict = {
        "num_of_items": len(posts),
        "items": posts
        }


        trade_template = jinja_env.get_template('templates/trading.html')
        self.response.write(trade_template.render(list_dict))

class WishlistHandler(webapp2.RequestHandler):
    def get(self):
        wish_template = jinja_env.get_template('templates/wishlist.html')
        self.response.write(wish_template.render())

class ThanksHandler(webapp2.RequestHandler):
    def get(self):
        thanks_template = jinja_env.get_template('templates/thank_you.html')
        self.response.write(thanks_template.render())

class NewPost(ndb.Model):
    image = ndb.BlobProperty()
    category = ndb.StringProperty(required=True)
    subcategory = ndb.StringProperty(required=True)
    title = ndb.StringProperty(required=True)
    price = ndb.StringProperty(required=True)
    description = ndb.StringProperty(required=True)
    communication = ndb.StringProperty(required=True)

class CreatePostHandler(webapp2.RequestHandler):
    def get(self):
        post_template = jinja_env.get_template('templates/create_post.html')
        self.response.write(post_template.render())

    def post(self):
        post_cat = self.request.get('cat')
        post_scat = self.request.get('subcat')
        post_title = self.request.get('titl')
        post_price = self.request.get('pric')
        post_comm = self.request.get('commun')
        post_pics = self.request.get('picture')
        # file_upload = self.request.POST.get("pics", None)
        post_desc = self.request.get('descrip')

        # new_name = NewPost(name=poster_name, item = post_item, paragraph = post_desc, image= file_upload.file.read())
        new_name = NewPost(category=post_cat, subcategory = post_scat, description = post_desc, title = post_title,
                            price = post_price, communication = post_comm,image= db.Blob(str(post_pics)))

        new_name.put()
        self.redirect('/thank_you')

class ImageHandler(webapp2.RequestHandler):
    def get(self):
        posts = NewPost.query().fetch()

        image_dict = {
        "num_of_items": len(posts)
        }
        index = self.request.get('index')
        index = int(index)
        posts[index].image
        if posts[index].image:
          self.response.headers['Content-Type'] = "image/jpg"
          self.response.out.write(posts[index].image)
        else:
          self.redirect('static/noimage.svg')


app = webapp2.WSGIApplication([
    ('/', HomepageHandler),
    ('/about_us', AboutUsHandler),
    ('/contact_us', ContactUsHandler),
    ('/selling', SellingHandler),
    ('/donate', DonateHandler),
    ('/freelance', FreelanceHandler),
    ('/trade', TradingHandler),
    ('/wishlist', WishlistHandler),
    ('/thank_you', ThanksHandler),
    ('/create_post', CreatePostHandler),
    ('/imageit', ImageHandler),
], debug=True)
