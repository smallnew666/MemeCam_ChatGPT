Page({
  data: {
    imageSrc:'点击上传照片',
    showIndex:0,//打开弹窗的对应下标
    showPage:1,//打开弹窗的对应下标
    height:0,//屏幕高度
    showRes:0,
    imageRes:'',
    showModal:0,
    task:null,
  },
  // 打开弹窗
  openPopup(){
    this.setData({
      showIndex:1
    })
  },
  //关闭弹窗
  closePopup(){
    this.setData({
      showIndex:0,
      imageSrc:'点击上传照片',
      imageRes:''

    })
  },
  closeRes(){
    this.setData({
      showIndex:0,//打开弹窗的对应下标
      showPage:1,//打开弹窗的对应下标
      height:0,//屏幕高度
      showRes:0,
      showModal:0,
      imageSrc:'点击上传照片',
      imageRes:''
    })
  },
  closeModal(){
    this.setData({
      showIndex:0,//打开弹窗的对应下标
      showPage:1,//打开弹窗的对应下标
      height:0,//屏幕高度
      showRes:0,
      showModal:0,
      imageSrc:'点击上传照片',
      imageRes:''
    })
    wx.hideLoading()
    this.getScreenHeight()
    this.data.task.abort()
  },
  onShareAppMessage() {         
    return {       
      title: 'AI爆梗相机', 
      desc: '制作你的爆款照片',     
      path: '/pages/index/index' // 路径，传递参数到指定页面。   
      }     
   },
   previewImage: function () {  
    wx.previewImage({
      urls: [this.data.imageRes],//需要预览的图片http链接列表，注意是数组形式
      current: this.data.imageRes,//当前显示图片的http链接，默认第一张
      success: function (res) {
        console.log(res)
      }
    })
  },
  openSave: function () {
    wx.showLoading({
      title: '保存中，请稍候...'
    });
    var that = this
    var aa = wx.getFileSystemManager();
    aa.writeFile({
      filePath:wx.env.USER_DATA_PATH+'/res.png',
      data: that.data.imageRes.slice(22),
      encoding:'base64',
      success: res => {
        wx.saveImageToPhotosAlbum({
          filePath: wx.env.USER_DATA_PATH + '/res.png',
          success: function (res) {
            console.log(res)
            wx.showToast({
              title: '保存成功',
            })
          },
          fail: function (err) {
            console.log(err)
            wx.showToast({
              title: '保存失败',
              icon: 'error',
              duration: 2000
            })
          }
        })
        console.log(res)
      }, fail: err => {
        console.log(err)
      }
    })
  },
  chooseImage: function () {
    const that = this
    wx.chooseMedia({
      count: 9,
      mediaType: ['image'],
      sourceType: ['album'],
      maxDuration: 30,
      camera: 'back',
      success(res) {
        that.setData({imageSrc:res.tempFiles[0].tempFilePath})
      }
    })
  },
  openCamera: function () {
    const that = this
    wx.chooseMedia({
      count: 9,
      mediaType: ['image'],
      sourceType: ['camera'],
      maxDuration: 30,
      camera: 'back',
      success(res) {
        that.setData({imageSrc:res.tempFiles[0].tempFilePath})
        console.log(res.tempFiles)
        that.openPopup()
      }
    })
  },
  uploadImage: function () {
    var that = this
    wx.showLoading({
      title: 'AI正在疯狂制作',
    })
    this.setData({
      showRes:1,
      showModal:1
    })
    const uploadTask = wx.uploadFile({
      url: '', // 替换为你的后端接口地址
      responseType: 'arraybuffer',
      filePath: that.data.imageSrc,
      name: 'image',
      success(res) {
        wx.hideLoading()
        // 处理后端返回的数据
        try {
          // 尝试执行可能会发生错误的代码
          var resdata = JSON.parse(res.data)
          that.setData({
            showPage:0,
            showRes:1,
            showIndex: 0,
            showModal:0,
            imageRes:resdata.data
           })
        } catch (err) {
          // 发生错误时的处理逻辑
          console.log('发生错误: ', err)
          wx.hideLoading()
          console.error(err);
          wx.showToast({
            title: '系统繁忙',
            icon: 'error',
            duration: 2000
          })
          that.setData({
            showIndex:0,//打开弹窗的对应下标
            showPage:1,//打开弹窗的对应下标
            height:0,//屏幕高度
            showRes:0,
            showModal:0,
            imageSrc:'点击上传照片',
            imageRes:''
          })
        }
      },
      fail: (err) => {
        wx.hideLoading()
        console.error(err);
        wx.showToast({
          title: '系统繁忙',
          icon: 'error',
          duration: 2000
        })
        that.setData({
          showIndex:0,//打开弹窗的对应下标
          showPage:1,//打开弹窗的对应下标
          height:0,//屏幕高度
          showRes:0,
          showModal:0,
          imageSrc:'点击上传照片',
          imageRes:''
        })
      }
    });
    this.setData({
      task:uploadTask,
    })
  },
  onLoad: function () {
    wx.showShareMenu({
      withShareTicket: true,
      menus: ['shareAppMessage', 'shareTimeline']
    })
  },
  getScreenHeight: function () {
    wx.getSystemInfo({
      success: (result) => {
        this.setData({
          height: result.windowHeight
        });
      },
      fail: (err) => {
        console.error(err);
      }
    });
  }
});
