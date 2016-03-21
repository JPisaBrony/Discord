function displayImages(dir, thumb_dir) {
        $.ajax({
            url: thumb_dir,
            success: function (data) {
                $(data).find("a").attr("href", function (i, val) {
                    if( val.match(/\.(jpe?g|png|gif)$/) ) {
                        $("body").append( "<img src='" + thumb_dir + "/" + val +"'>" );
                    }
                });
                $("img").click(function(){
                    var url = this.src.replace(thumb_dir, dir);
                    var type = url.split(".").pop();
                    var name = url.split("/")[4];
                    var x = new XMLHttpRequest();
                    x.open("GET", url, true);
                    x.responseType = "blob";
                    x.onload = function(e) {
                        download(x.response, name, dir + "/" + type);
                    }
                    x.send();
                });
            }
        }); 
}

$(document).ready(function() {
    $('#navbar').load('navbar.html');
});
