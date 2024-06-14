
/*
Tipr 2.0.1
Copyright (c) 2015 Tipue
Tipr is released under the MIT License
http://www.tipue.com/tipr
*/

(function ($) {
    $.fn.tipr = function (options) {
        var set = $.extend({ 'speed': 200, 'mode': 'bottom' }, options); return this.each(function () {
            var tipr_cont = '.tipr_container_' + set.mode; $(this).hover(function () {
                var d_m = set.mode; if ($(this).attr('data-mode')) {
                    d_m = $(this).attr('data-mode')
                    tipr_cont = '.tipr_container_' + d_m;
                }
                var out = '<div class="tipr_container_' + d_m + '"><div class="tipr_point_' + d_m + '"><div class="tipr_content">' + $(this).attr('data-tip') + '</div></div></div>'; $(this).append(out); var w_t = $(tipr_cont).outerWidth(); var w_e = $(this).width(); var m_l = (w_e / 2) - (w_t / 2); $(tipr_cont).css('margin-left', m_l + 'px'); $(this).removeAttr('title alt'); $(tipr_cont).fadeIn(set.speed);
            }, function ()
            { $(tipr_cont).remove(); });
        });
    };
})(jQuery);


//-------------------------------------------------------------------------------------------------------------------

/*!
 * jQuery Cookie Plugin v1.4.1
 * https://github.com/carhartl/jquery-cookie
 *
 * Copyright 2006, 2014 Klaus Hartl
 * Released under the MIT license
 */
!function (a) { "function" == typeof define && define.amd ? define(["jquery"], a) : "object" == typeof exports ? module.exports = a(require("jquery")) : a(jQuery) }(function (a) { function c(a) { return h.raw ? a : encodeURIComponent(a) } function d(a) { return h.raw ? a : decodeURIComponent(a) } function e(a) { return c(h.json ? JSON.stringify(a) : String(a)) } function f(a) { 0 === a.indexOf('"') && (a = a.slice(1, -1).replace(/\\"/g, '"').replace(/\\\\/g, "\\")); try { return a = decodeURIComponent(a.replace(b, " ")), h.json ? JSON.parse(a) : a } catch (a) { } } function g(b, c) { var d = h.raw ? b : f(b); return a.isFunction(c) ? c(d) : d } var b = /\+/g, h = a.cookie = function (b, f, i) { if (arguments.length > 1 && !a.isFunction(f)) { if (i = a.extend({}, h.defaults, i), "number" == typeof i.expires) { var j = i.expires, k = i.expires = new Date; k.setMilliseconds(k.getMilliseconds() + 864e5 * j) } return document.cookie = [c(b), "=", e(f), i.expires ? "; expires=" + i.expires.toUTCString() : "", i.path ? "; path=" + i.path : "", i.domain ? "; domain=" + i.domain : "", i.secure ? "; secure" : ""].join("") } for (var l = b ? void 0 : {}, m = document.cookie ? document.cookie.split("; ") : [], n = 0, o = m.length; n < o; n++) { var p = m[n].split("="), q = d(p.shift()), r = p.join("="); if (b === q) { l = g(r, f); break } b || void 0 === (r = g(r)) || (l[q] = r) } return l }; h.defaults = {}, a.removeCookie = function (b, c) { return a.cookie(b, "", a.extend({}, c, { expires: -1 })), !a.cookie(b) } });


//-------------------------------------------------------------------------------------------------------------------

/*  jQuery Nice Select - v1.0
    https://github.com/hernansartorio/jquery-nice-select
    Made by Hernán Sartorio  */
!function (e) { e.fn.niceSelect = function (t) { function s(t) { t.after(e("<div></div>").addClass("nice-select").addClass(t.attr("class") || "").addClass(t.attr("disabled") ? "disabled" : "").attr("tabindex", t.attr("disabled") ? null : "0").html('<span class="current"></span><ul class="list"></ul>')); var s = t.next(), n = t.find("option"), i = t.find("option:selected"); s.find(".current").html(i.data("display") || i.text()), n.each(function (t) { var n = e(this), i = n.data("display"); s.find("ul").append(e("<li></li>").attr("data-value", n.val()).attr("data-display", i || null).addClass("option" + (n.is(":selected") ? " selected" : "") + (n.is(":disabled") ? " disabled" : "")).html(n.text())) }) } if ("string" == typeof t) return "update" == t ? this.each(function () { var t = e(this), n = e(this).next(".nice-select"), i = n.hasClass("open"); n.length && (n.remove(), s(t), i && t.next().trigger("click")) }) : "destroy" == t ? (this.each(function () { var t = e(this), s = e(this).next(".nice-select"); s.length && (s.remove(), t.css("display", "")) }), 0 == e(".nice-select").length && e(document).off(".nice_select")) : console.log('Method "' + t + '" does not exist.'), this; this.hide(), this.each(function () { var t = e(this); t.next().hasClass("nice-select") || s(t) }), e(document).off(".nice_select"), e(document).on("click.nice_select", ".nice-select", function (t) { var s = e(this); e(".nice-select").not(s).removeClass("open"), s.toggleClass("open"), s.hasClass("open") ? (s.find(".option"), s.find(".focus").removeClass("focus"), s.find(".selected").addClass("focus")) : s.focus() }), e(document).on("click.nice_select", function (t) { 0 === e(t.target).closest(".nice-select").length && e(".nice-select").removeClass("open").find(".option") }), e(document).on("click.nice_select", ".nice-select .option:not(.disabled)", function (t) { var s = e(this), n = s.closest(".nice-select"); n.find(".selected").removeClass("selected"), s.addClass("selected"); var i = s.data("display") || s.text(); n.find(".current").text(i), n.prev("select").val(s.data("value")).trigger("change") }), e(document).on("keydown.nice_select", ".nice-select", function (t) { var s = e(this), n = e(s.find(".focus") || s.find(".list .option.selected")); if (32 == t.keyCode || 13 == t.keyCode) return s.hasClass("open") ? n.trigger("click") : s.trigger("click"), !1; if (40 == t.keyCode) { if (s.hasClass("open")) { var i = n.nextAll(".option:not(.disabled)").first(); i.length > 0 && (s.find(".focus").removeClass("focus"), i.addClass("focus")) } else s.trigger("click"); return !1 } if (38 == t.keyCode) { if (s.hasClass("open")) { var l = n.prevAll(".option:not(.disabled)").first(); l.length > 0 && (s.find(".focus").removeClass("focus"), l.addClass("focus")) } else s.trigger("click"); return !1 } if (27 == t.keyCode) s.hasClass("open") && s.trigger("click"); else if (9 == t.keyCode && s.hasClass("open")) return !1 }); var n = document.createElement("a").style; return n.cssText = "pointer-events:auto", "auto" !== n.pointerEvents && e("html").addClass("no-csspointerevents"), this } }(jQuery);

//-------------------------------------------------------------------------------------------------------------------

