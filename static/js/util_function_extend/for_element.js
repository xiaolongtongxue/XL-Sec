/**
 * 该扩展方法的意义在于使得textarea标签得以由于输入内容的变多变少实现自动扩展。
 * 使用方法：
 * ```html
 * inclue(此文件);
 * $('textarea').autoHeight();
 * ```
 */
jQuery.fn.extend({
    autoHeight: function () {
        return this.each(function () {
            var $this = jQuery(this);
            if (!$this.attr('_initAdjustHeight')) {
                $this.attr('_initAdjustHeight', $this.outerHeight());
            }
            _adjustH(this).on('input', function () {
                _adjustH(this);
            });
        });
        
        function _adjustH(elem) {
            var $obj = jQuery(elem);
            return $obj.css({height: $obj.attr('_initAdjustHeight'), 'overflow-y': 'hidden'}).height(elem.scrollHeight);
        }
    }
});