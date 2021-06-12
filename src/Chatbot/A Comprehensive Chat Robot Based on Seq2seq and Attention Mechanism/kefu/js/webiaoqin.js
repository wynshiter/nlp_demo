// 原 swipe.js文件
  window.Swipe = function(element, options) {
    if (!element) return null;
    var _this = this;
    this.options = options || {};
    this.index = this.options.startSlide || 0;
    this.speed = this.options.speed || 300;
    this.callback = this.options.callback ||
    function() {};
    this.container = element;
    this.element = this.container.children[0];
    this.element.style.listStyle = 'none';
    this.setup();
    this.begin();
    if (this.element.addEventListener) {
      this.element.addEventListener('mousedown', this, false);
      this.element.addEventListener('touchstart', this, false);
      this.element.addEventListener('touchmove', this, false);
      this.element.addEventListener('touchend', this, false);
      this.element.addEventListener('webkitTransitionEnd', this, false);
      this.element.addEventListener('msTransitionEnd', this, false);
      this.element.addEventListener('oTransitionEnd', this, false);
      this.element.addEventListener('transitionend', this, false);
      if (!this.unresize) {
        window.addEventListener('resize', this, false)
      }
    }
  };
  Swipe.prototype = {
    setup: function() {
      this.slides = this.element.children;
      this.length = this.slides.length;
      if (this.length < 2) return null;
      this.width = this.container.getBoundingClientRect().width || this.width;
      if (!this.width) return null;
      this.container.style.visibility = 'hidden';
      this.element.style.width = (this.slides.length * this.width) + 'px';
      var index = this.slides.length;
      while (index--) {
        var el = this.slides[index];
        el.style.width = this.width + 'px';
        el.style.display = 'table-cell';
        el.style.verticalAlign = 'top'
      }
      this.slide(this.index, 0);
      this.container.style.visibility = 'visible'
    },
    slide: function(index, duration) {
      var style = this.element.style;
      if (duration == undefined) {
        duration = this.speed
      }
      style.webkitTransitionDuration = style.MozTransitionDuration = style.msTransitionDuration = style.OTransitionDuration = style.transitionDuration = duration + 'ms';
      style.MozTransform = style.webkitTransform = 'translate3d(' + -(index * this.width) + 'px,0,0)';
      style.msTransform = style.OTransform = 'translateX(' + -(index * this.width) + 'px)';
      this.index = index
    },
    getPos: function() {
      return this.index
    },
    prev: function(delay) {
      this.delay = delay || 0;
      clearTimeout(this.interval);
      if (this.index) this.slide(this.index - 1, this.speed)
    },
    next: function(delay) {
      this.delay = delay || 0;
      clearTimeout(this.interval);
      if (this.index < this.length - 1) this.slide(this.index + 1, this.speed);
      else this.slide(0, this.speed)
    },
    begin: function() {
      var _this = this;
      this.interval = (this.delay) ? setTimeout(function() {
        _this.next(_this.delay)
      }, this.delay) : 0
    },
    stop: function() {
      this.delay = 0;
      clearTimeout(this.interval)
    },
    resume: function() {
      this.delay = this.options.auto || 0;
      this.begin()
    },
    handleEvent: function(e) {
      var that = this;
      if (!e.touches) {
        e.touches = new Array(e);
        e.scale = false
      }
      switch (e.type) {
      case 'mousedown':
        (function() {
          that.element.addEventListener('mousemove', that, false);
          that.element.addEventListener('mouseup', that, false);
          that.element.addEventListener('mouseout', that, false);
          that.onTouchStart(e)
        })();
        break;
      case 'mousemove':
        this.onTouchMove(e);
        break;
      case 'mouseup':
        (function() {
          that.element.removeEventListener('mousemove', that, false);
          that.element.removeEventListener('mouseup', that, false);
          that.element.removeEventListener('mouseout', that, false);
          that.onTouchEnd(e)
        })();
        break;
      case 'mouseout':
        (function() {
          that.element.removeEventListener('mousemove', that, false);
          that.element.removeEventListener('mouseup', that, false);
          that.element.removeEventListener('mouseout', that, false);
          that.onTouchEnd(e)
        })();
        break;
      case 'touchstart':
        this.onTouchStart(e);
        break;
      case 'touchmove':
        this.onTouchMove(e);
        break;
      case 'touchend':
        this.onTouchEnd(e);
        break;
      case 'webkitTransitionEnd':
      case 'msTransitionEnd':
      case 'oTransitionEnd':
      case 'transitionend':
        this.transitionEnd(e);
        break;
      case 'resize':
        this.setup();
        break
      }
    },
    transitionEnd: function(e) {
      e.preventDefault();
      if (this.delay) this.begin();
      this.callback(e, this.index, this.slides[this.index])
    },
    onTouchStart: function(e) {
      this.start = {
        pageX: e.touches[0].pageX,
        pageY: e.touches[0].pageY,
        time: Number(new Date())
      };
      this.isScrolling = undefined;
      this.deltaX = 0;
      this.element.style.MozTransitionDuration = this.element.style.webkitTransitionDuration = 0
    },
    onTouchMove: function(e) {
      if (e.touches.length > 1 || e.scale && e.scale !== 1) return;
      this.deltaX = e.touches[0].pageX - this.start.pageX;
      if (typeof this.isScrolling == 'undefined') {
        this.isScrolling = !! (this.isScrolling || Math.abs(this.deltaX) < Math.abs(e.touches[0].pageY - this.start.pageY))
      }
      if (!this.isScrolling) {
        e.preventDefault();
        clearTimeout(this.interval);
        this.deltaX = this.deltaX / ((!this.index && this.deltaX > 0 || this.index == this.length - 1 && this.deltaX < 0) ? (Math.abs(this.deltaX) / this.width + 1) : 1);
        this.element.style.MozTransform = this.element.style.webkitTransform = 'translate3d(' + (this.deltaX - this.index * this.width) + 'px,0,0)'
      }
    },
    onTouchEnd: function(e) {
      var isValidSlide = Number(new Date()) - this.start.time < 250 && Math.abs(this.deltaX) > 20 || Math.abs(this.deltaX) > this.width / 2,
        isPastBounds = !this.index && this.deltaX > 0 || this.index == this.length - 1 && this.deltaX < 0;
      if (!this.isScrolling) {
        this.slide(this.index + (isValidSlide && !isPastBounds ? (this.deltaX < 0 ? 1 : -1) : 0), this.speed)
      }
    }
  };
// 原 input.js文件
  var myInput = (function() {
    var mi = function() {
        this.maxLength = 500, this.currentLength = 0
      }
    mi.prototype = {
      listen: function(thi, evt) {
        var that = this;
        if ("/:del" == evt.value) {
          thi = evt.srcElement;
          var imgs = thi.querySelectorAll("img");
          if (imgs.length) {
            imgs[imgs.length - 1].remove()
          }
          return
        }
        if (evt.keyCode && -10 == evt.keyCode) {
          if (evt.value.length > (that.maxLength - that.currentLength)) {
            return that
          }
          thi = evt.srcElement;
          var img = new Image();
          img.src = evt.imgUrl;
          img.innerHTML = evt.value;
          img.setAttribute("data-innerHTML", evt.value);
          thi.appendChild(img)
        }
      }
    }
    return new mi()
  })();
// 原 dialog_min.js文件
  var iDialog = (function() {
    var a = function() {
        this.options = {
          id: "dialogWindow_",
          classList: "",
          type: "",
          wrapper: "",
          title: "",
          close: "",
          content: "",
          cover: true,
          btns: []
        }
      };
    return a
  })();
  var iTemplate = (function() {
    var a = function() {};
    a.prototype = {
      makeList: function(e, j, i) {
        var g = [],
          h = [],
          c = /{(.+?)}/g,
          d = {},
          f = 0;
        for (var b in j) {
          if (typeof i === "function") {
            d = i.call(this, b, j[b], f++) || {}
          }
          g.push(e.replace(c, function(k, l) {
            return (l in d) ? d[l] : (undefined === j[b][l] ? j[b] : j[b][l])
          }))
        }
        return g.join("")
      }
    };
    return new a()
  })();
// 原index.html文件内部js
  $().ready(function() {
    form_emotion.rend();
    myInput.maxLength = 500
  });
  var form_emotion = (function() {
    var fe = function() {
        this.values = ["/::)", "/::~", "/::B", "/::|", "/:8-)", "/::<", "/::$", "/::X", "/::Z", "/::'(", "/::-|", "/::@", "/::P", "/::D", "/::O", "/::(", "/::+", "/:–b", "/::Q", "/::T", "/:,@P", "/:,@-D", "/::d", "/:,@o", "/::g", "/:|-)", "/::!", "/::L", "/::>", "/::,@", "/:,@f", "/::-S", "/:?", "/:,@x", "/:,@@", "/::8", "/:,@!", "/:!!!", "/:xx", "/:bye", "/:wipe", "/:dig", "/:handclap", "/:&-(", "/:B-)", "/:<@", "/:@>", "/::-O", "/:>-|", "/:P-(", "/::'|", "/:X-)", "/::*", "/:@x", "/:8*", "/:pd", "/:<W>", "/:beer", "/:basketb", "/:oo", "/:coffee", "/:eat", "/:pig", "/:rose", "/:fade", "/:showlove", "/:heart", "/:break", "/:cake", "/:li", "/:bome", "/:kn", "/:footb", "/:ladybug", "/:shit", "/:moon", "/:sun", "/:gift", "/:hug", "/:strong", "/:weak", "/:share", "/:v", "/:@)", "/:jj", "/:@@", "/:bad", "/:lvu", "/:no", "/:ok", "/:love", "/:<L>", "/:jump", "/:shake", "/:<O>", "/:circle", "/:kotow", "/:turn", "/:skip", "[挥手]", "/:#-0", "[街舞]", "/:kiss", "/:<&", "/:&>"].slice(0, -7);
        this.spearate = 20
      }
    fe.prototype = {
      rend: function() {
        var that = this;
        var TPL = '{seprateDiv}<p><span data-key="{k}_{page}_{v}" style="background-image:url(./images/arclist/{k}.gif)"></span></p>{delHTML}';
        var res = iTemplate.makeList(TPL, that.values, function(k, v) {
          return {
            k: k,
            v: v,
            page: Math.floor(k / that.spearate),
            xPos: -24 * k,
            seprateDiv: (0 == k % that.spearate && 0 != k && k != that.values.length) ? "</div><div>" : "",
            delHTML: (19 == k % that.spearate || k == (that.values.length - 1)) ? '<p><span data-key="-1_-1_/:del" class="del"></span></p>' : ''
          }
        });
        $("#list_emotion").html('<div>' + res + '</div>');
        var nav_span = new Array(Math.ceil(that.values.length / that.spearate));
        $("#nav_emotion").html('<span class="on">' + nav_span.join("</span><span>") + '</span>');
        that.bind();
        window.swiper = new Swipe(document.getElementById('page_emotion'), {
          speed: 500,
          callback: function() {
            $("#nav_emotion span").removeClass("on").eq(this.index).addClass("on")
          }
        });
        return that
      },
      bind: function() {
        $("#list_emotion").on("click", function(evt) {
          if ("SPAN" == evt.target.tagName) {
            var val = evt.target.getAttribute("data-key").split('_');
            myInput.listen(this, {
              keyCode: -10,
              srcElement: document.getElementById("form_article"),
              value: val[2],
              imgUrl: 'images/arclist/' + val[0] + ".gif"
            });
            this.focus()
          }
        })
      }
    }
    return new fe()
  })();