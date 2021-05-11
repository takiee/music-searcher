<template>
  <div :class="{content: true, ellipsis: ellipsis}">
    {{content}}
  </div>
</template>

<script>
export default {
  data () {
    return {
      content: '这里是测试的文字，abc,123,这里是测试的文字，abc,123,这里是测试的文字，abc,123',
      ellipsis: false // 判断是否要加上...的样式
    }
  },
  create () {
    if (this.content && this.content.trim()) {
      const contentWidth = 800 // 假设原来文本的宽度的800，这里根据具体的情况而定
      this.ellipsis = this.isEllipsis(this.content.trim(), contentWidth)
    }
  },
  method: {
    isEllipsis (content, contentWidth) {
      let el = document.createElement('div')  // 创建一个临时div
      el.innerHTML = content
      el.style.whiteSpace = 'nowrap' // 不换行
      el.style.position = 'absolute'
      el.style.opacity = 0 // 完全透明
      document.body.appendChild(el)
      const elWidth = el.clientWidth  // 获取这个含有content内容的临时div的宽度
      document.body.removeChild(el)
      return elWidth >= contentWidth * 2   // 判断这个临时div的宽度是否大于原节点宽度的两倍
    }
  }
}
</script>

<style lang="scss">
  .content {
    max-height: 45px;  // 两行文字的最大高度
    line-height: 22px;
    overflow: hidden;
    position: relative;
    &.ellipsis {
      &:after {       // 如果超过2行的宽度，则用...放在第二行的结尾
        content: '...';
        font-weight: bold;
        position: absolute; // 调整...的位置
        top: 22px;
        right: 0;
        padding: 0 20px 1px 45px;
        background: url('../images/ellipsis_bg.png') repeat-y;   // 预先准备好的覆盖的尾部图片
      }
    }
  }
</style>

