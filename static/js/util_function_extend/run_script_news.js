/**
 * 
 * @param {容器的容器ID，一般传入 document.getElementByID('xxx') 就可以啦} container 
 * @param {需要加入的HTML代码，这里边如果有js语句的话则会在加入的时候直接执行，从而解决相关问题} rawHTML 
 */
function setHTMLWithScript(container, rawHTML){
    container.innerHTML = rawHTML;
    const scripts = container.querySelectorAll('script');
    for (let script of scripts) {
        const newScript = document.createElement('script');
        newScript.innerHTML = script.innerHTML;
        const src = script.getAttribute('src');
        if (src) newScript.setAttribute('src', src);
        document.body.appendChild(newScript);
        document.body.removeChild(newScript);
    }
}