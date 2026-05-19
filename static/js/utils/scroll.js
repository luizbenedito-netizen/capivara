window.onload = function() {

    const container = document.querySelector(".layout");
    const thumb = document.getElementById("thumb");
    const scrollbar = document.getElementById("scrollbar");

    function updateThumb() {

        // if (window.innerWidth <= 768) {
        //     if (scrollbar) scrollbar.style.display = "none";
        //         return;
        // }
        // scrollbar.style.display = "block";

        const totalHeight = container.scrollHeight;
        const visibleHeight = container.clientHeight;
        const trackHeight = scrollbar.clientHeight;

        if (totalHeight <= visibleHeight) {
            thumb.style.opacity = "0";
            return;
        } else {
            thumb.style.opacity = "1";
        }

        const ratio = visibleHeight / totalHeight;
        let thumbHeight = ratio * trackHeight;
        thumbHeight = Math.max(thumbHeight, 30);
        thumb.style.height = thumbHeight + "px";

        const scrollLimit = totalHeight - visibleHeight;
        const scrollRatio = container.scrollTop / scrollLimit;
        
        const trackLimit = trackHeight - thumbHeight;
        const topPosition = scrollRatio * trackLimit;
        
        thumb.style.top = topPosition + "px";
    }

    container.addEventListener("scroll", updateThumb);
    window.addEventListener("resize", updateThumb);
    
    setTimeout(updateThumb, 100);

    let isDragging = false;
    let startY, startTop;

    thumb.addEventListener("mousedown", (e) => {
        isDragging = true;
        startY = e.clientY;
        startTop = thumb.offsetTop;
        document.body.style.userSelect = "none";
    });

    document.addEventListener("mousemove", (e) => {
        if (!isDragging) return;
        
        const deltaY = e.clientY - startY;
        const trackHeight = scrollbar.clientHeight;
        const thumbHeight = thumb.clientHeight;
        
        let newTop = startTop + deltaY;
        newTop = Math.max(0, Math.min(newTop, trackHeight - thumbHeight));
        
        const scrollRatio = newTop / (trackHeight - thumbHeight);
        container.scrollTop = scrollRatio * (container.scrollHeight - container.clientHeight);
    });

    document.addEventListener("mouseup", () => {
        isDragging = false;
        document.body.style.userSelect = "";
    });
};