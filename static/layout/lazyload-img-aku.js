!function(e, t) {
    "function" == typeof define && define.amd ? define(function() {
        return t(e)
    }) : "object" == typeof exports ? module.exports = t : e.progressively = t(e)
}(this, function(e) {
    "use strict";
    function t(e, t) {
        var n = {};
        for (var o in e)
            n[o] = t.hasOwnProperty(o) ? t[o] : e[o];
        return n
    }
    function n(e) {
        var t = e.getBoundingClientRect()
          , n = t.top
          , o = t.height;
        e = e.parentNode;
        do {
            if (t = e.getBoundingClientRect(),
            !(n <= t.bottom))
                return !1;
            if (n + o <= t.top)
                return !1;
            e = e.parentNode
        } while (e !== document.body && e !== document);return n <= document.documentElement.clientHeight
    }
    function o(e, t) {
        setTimeout(function() {
            var n = new Image;
            n.onload = function() {
                e.classList.remove("progressive--not-loaded"),
                e.classList.add("progressive--is-loaded"),
                e.classList.contains("progressive__bg") ? e.style["background-image"] = 'url("' + this.src + '")' : e.src = this.src,
                d(e)
            }
            ,
            r() <= t.smBreakpoint && e.getAttribute("data-progressive-sm") ? (e.classList.add("progressive--loaded-sm"),
            n.src = e.getAttribute("data-progressive-sm")) : (e.classList.remove("progressive--loaded-sm"),
            n.src = e.getAttribute("data-progressive"))
        }, t.delay)
    }
    function r() {
        return Math.max(document.documentElement.clientWidth, window.innerWidth || 0)
    }
    function i() {
        c || (clearTimeout(c),
        c = setTimeout(function() {
            l.check(),
            l.render(),
            c = null
        }, s.throttle))
    }
    var s, c, d, a, l = {};
    return d = function() {}
    ,
    s = {
        throttle: 300,
        delay: 100,
        onLoadComplete: function() {},
        onLoad: function() {},
        smBreakpoint: 600
    },
    l.init = function(n) {
        n = n || {},
        s = t(s, n),
        d = s.onLoad || d,
        a = [].slice.call(document.querySelectorAll(".progressive__img, .progressive__bg")),
        l.render(),
        document.addEventListener ? (e.addEventListener("scroll", i, !1),
        e.addEventListener("resize", i, !1),
        e.addEventListener("load", i, !1)) : (e.attachEvent("onscroll", i),
        e.attachEvent("onresize", i),
        e.attachEvent("onload", i))
    }
    ,
    l.render = function() {
        for (var e, t = a.length - 1; t >= 0; --t)
            e = a[t],
            n(e) && e.classList.contains("progressive--not-loaded") && (o(e, s),
            a.splice(t, 1));
        this.check()
    }
    ,
    l.check = function() {
        a.length || (s.onLoadComplete(),
        this.drop())
    }
    ,
    l.drop = function() {
        document.removeEventListener ? (e.removeEventListener("scroll", i),
        e.removeEventListener("resize", i)) : (e.detachEvent("onscroll", i),
        e.detachEvent("onresize", i)),
        clearTimeout(c)
    }
    ,
    l
});
