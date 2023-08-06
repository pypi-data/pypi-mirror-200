#pylint:disable=E0211
from requests import get,post
from rabino.encryption import encryption
from random import randint, choice
from rabino.How import *
from rabino.server import Server
from pathlib import Path
from json import loads,dumps


class rubino:
	def __init__(self, auth):
		self.auth = auth
		self.print = chup.x_coder
		
	def _getUrl():
		return choice(Server.rubino)
		
		
	def _request(self,inData,method):
		data = {"api_version": "0","auth": self.auth,"client": {"app_name": "Main","app_version": "3.0.2","lang_code": "fa","package": "app.rbmain.a","platform": "Android"},"data": inData,"method": method}
		while True:
			try:
				return post(rubino._getUrl(),json=data).json()
			except:
				continue
	
	
	
	def follow(self,followee_id,profile_id=None):
		inData = {"f_type": "Follow","followee_id": followee_id,"profile_id": profile_id}
		method = 'requestFollow'
		while True:
			try:
				return self._request(inData,method)
			except:continue
		
		
	def getPostByShareLink(self,link,profile_id=None):
		if link.startswith("post/"):
			print(link)
			god = link.split("post/")
			print(link)
			inData = {"share_string":god,"profile_id":profile_id}
		else:
			inData = {"share_string":link,"profile_id":profile_id}
		method = "getPostByShareLink"
		while True:
			try:
				return self._request(inData,method).get('data')
			except:continue
			
			
	def addPostViewCount(self,post_id,post_target_id):
		inData = {"post_id":post_id,"post_profile_id":post_target_id}
		method = "addPostViewCount"
		while True:
			try:
				return self._request(inData,method)
			except:continue
	
	def getProfileStories(self,prof=None):
		inData = {"limit": 100, "profile_id": prof}
		method = "getProfileStories"
		while True:
			try:
				return self._request(inData,method)
			except:continue
	
	def requestUploadFile(self,file,size=None, Type="Picture",prof=None):
		inData = {
			"file_name": file.split("/")[-1],
			"file_size": size or Path(file).stat().st_size, 
			"file_type": Type,
			"profile_id": prof}
		method = "requestUploadFile"
		while True:
			try:
				return self._request(inData,method)
			except:continue
			
	@staticmethod
	def _getThumbInline(image_bytes:bytes):
		import io, base64, PIL.Image
		im = PIL.Image.open(io.BytesIO(image_bytes))
		width, height = im.size
		if height > width:
			new_height = 40
			new_width  = round(new_height * width / height)
		else:
			new_width  = 40
			new_height = round(new_width * height / width)
		im = im.resize((new_width, new_height), PIL.Image.ANTIALIAS)
		changed_image = io.BytesIO()
		im.save(changed_image, format='PNG')
		changed_image = changed_image.getvalue()
		return base64.b64encode(changed_image)

	@staticmethod
	def _getImageSize(image_bytes:bytes):
		import io, PIL.Image
		im = PIL.Image.open(io.BytesIO(image_bytes))
		width, height = im.size
		return [width , height]
	
	def upload(self,file,Type):
		if not "http" in file:
			REQUEST = self.requestUploadFile(file)["data"]
			bytef = open(file,"rb").read()
			file_id = REQUEST["file_id"]
			hash_send = REQUEST["hash_file_request"]
			url = REQUEST["server_url"]
			header = {
				'auth':self.auth,
				'Host':url.replace("https://","").replace("/UploadFile.ashx",""),
				'chunk-size':str(Path(file).stat().st_size),
				'file-id':str(file_id),
				'hash-file-request':hash_send,
				"content-type": "application/octet-stream",
				"content-length": str(Path(file).stat().st_size),
				"accept-encoding": "gzip",
				"user-agent": "okhttp/3.12.1",
				"part-number":"1",
				"total-part":"1"}
			j = post(data=bytef,url=url,headers=header).text
			j = loads(j)['data']['hash_file_receive']


			return [REQUEST, j]
		else:
			REQUEST = {
			"file_name": file.split("/")[-1],
			"file_size": size or Path(file).stat().st_size, 
			"file_type": Type,
			"profile_id": ""}
			method = "requestUploadFile"
			while True:
				try:
					return self._request(inData,method)
				except:continue
				bytef = get(file).content
				file_id = REQUEST["file_id"]
				hash_send = REQUEST["hash_file_request"]
				url = REQUEST["server_url"]
				header = {
				'auth':self.auth,
				'Host':url.replace("https://","").replace("/UploadFile.ashx",""),
				'chunk-size':str(Path(file).stat().st_size),
				'file-id':str(file_id),
				'hash-file-request':hash_send,
				"content-type": "application/octet-stream",
				"content-length": str(Path(file).stat().st_size),
				"accept-encoding": "gzip",
				"user-agent": "okhttp/3.12.1",
				"part-number":"1",
				"total-part":"1"}
				j = post(data=bytef,url=url,headers=header).text
				j = loads(j)['data']['hash_file_receive']
				return [REQUEST, j]
	
	
	def getStoryIds(self,target_profile_id,profile_id=None):
		inData = {"profile_id":profile_id,"target_profile_id":target_profile_id}
		method = 'getStoryIds'
		while True:
			try:
				return self._request(inData,method)
			except:continue
			
	def getComments(self,post_id,post_prof,prof=None):
		inData = {"equal": False, "limit": 100, "sort": "FromMax", "post_id": post_id, "profile_id": prof, "post_profile_id": post_prof}
		method = "getComments"
		while True:
			try:
				return self._request(inData,method)
			except:continue
	
	def updateProfile(self,profile_id=None):
		inData = {"profile_id":profile_id,"profile_status":"Public"}
		method = 'updateProfile'
		while True:
			try:
				return self._request(inData,method)
			except:continue
			
	def addPost(self,file,caption=None,is_multi_file=None,post_type="Picture",prof=None):
		urespone = self.upload(file,post_type)
		hashFile = urespone[1]
		fileID = urespone[0]["file_id"]
		thumbnailID = urespone[0]["file_id"]
		thumbnailHash = urespone[1]
		inData = {"caption": caption, "file_id": fileID, "hash_file_receive": hashFile, "height": 800, "width": 800, "is_multi_file": is_multi_file, "post_type": post_type, "rnd": randint(100000, 999999999), "thumbnail_file_id": thumbnailID, "thumbnail_hash_file_receive": thumbnailHash, "profile_id": prof}
		method = "addPost"
		while True:
			try:
				return self._request(inData,method)
			except:continue
	def getRecentFollowingPosts(self,profile_id=None):
		inData = {"equal":False,"limit":30,"sort":"FromMax","profile_id":profile_id}
		method = 'getRecentFollowingPosts'
		while True:
			try:
				return self._request(inData,method)
			except:continue
			
			
	def getProfileList(self):
		inData = {"equal":False,"limit":10,"sort":"FromMax"}
		method = 'getProfileList'
		while True:
			try:
				return self._request(inData,method)
			except:continue
			
			
	def getMyProfileInfo(self,profile_id=None):
		inData = {"profile_id":profile_id}
		method = 'getMyProfileInfo'
		while True:
			try:
				return self._request(inData,method)
			except:continue
			
			
	def Like(self,post_id,target_post,prof=None):
		inData ={"action_type":"Like","post_id":post_id,"post_profile_id":target_post,"profile_id":prof}
		method = 'likePostAction'
		while True:
			try:
				return self._request(inData,method)
			except:continue
			
	def getShareLink(self,post_id,post_profile,prof=None):
		inData = {"post_id":post_id,"post_profile_id":post_profile,"profile_id":prof}
		method = 'getShareLink'
		while True:
			try:
				return self._request(inData,method)
			except:continue
	
	def isExistUsername(self,username):
		if username.startswith("@"):
			username = username.split("@")[1]
			inData = {"username": username}
		else:
			inData = {"username": username}
		method = "isExistUsername"
		while True:
			try:
				return self._request(inData,method)
			except:continue
			
	def addViewStory(self,story,ids,prof=None):
		indata = {"profile_id":prof,"story_ids":[ids],"story_profile_id":story}
		method = 'addViewStory'
		while True:
			try:
				return self._request(indata,method)
			except:continue
			
			
	def createPage(self,name,username,bio=None):
		inData = {"bio": bio,"name": name,"username": username}
		method = 'createPage'
		while True:
			try:
				return self._request(inData,method)
			except:continue
			
			
	def comment(self,text,poat_id,post_target,prof=None):
		inData = {"content": text,"post_id": poat_id,"post_profile_id": post_target,"rnd":f"{randint(100000,999999999)}" ,"profile_id":prof}
		method = 'addComment'
		while True:
			try:
				return self._request(inData,method)
			except:continue
		
		
	def UnLike(self,post_id,post_profile_id,prof=None):
		inData = {"action_type":"Unlike","post_id":post_id,"post_profile_id":post_profile_id,"profile_id":prof}
		method ='likePostAction'
		while True:
			try:
				return self._request(inData,method)
			except:continue
			
			
	def sevaePost(self,post_id,post_profile_id,prof=None):
		inData = {"action_type":"Bookmark","post_id":post_id,"post_profile_id":post_profile_id,"profile_id":prof}
		method ='postBookmarkAction'
		while True:
			try:
				return self._request(inData,method)
			except:continue

