function DiscordViewModel() {
    var self = this;
    
    self.navs = ko.observableArray();
    self.navs.push("<a class='pure-menu-link'>Home</a>");
    self.navs.push("<a class='pure-menu-link'>SFW Pony</a>");
    self.navs.push("<a class='pure-menu-link'>NSFW Pony</a>");
    self.navs.push("<a class='pure-menu-link'>SFW Furry</a>");
    self.navs.push("<a class='pure-menu-link'>NSFW Furry</a>");
    
    self.homepage = "<div class='pure-g'><div class='pure-u-1-3'></div><div class='pure-u-1-3 main-title'><p>JPisaBrony's Discord Gallery Mirror</p></div><div class='pure-u-1-3'></div></div><div class='wrap'><div class='cube'><div class='front'><img src='cube/twi.png' width=180px height=180px></div><div class='back'><img src='cube/apple.png' width=180px height=180px></div><div class='top'><img src='cube/rar.png' width=180px height=180px></div><div class='bottom'><img src='cube/flut.png' width=180px height=180px></div><div class='left'><img src='cube/pinkie.png' width=180px height=180px></div><div class='right'><img src='cube/rainbow.png' width=180px height=180px></div></div></div>";
    
    self.pageData = ko.observable(self.homepage);
    
    self.changeNav = function(sel) {
        var page = sel.split(">");
        page = page[1].split("<");
        
        if(page[0] == "Home") {
            self.pageData(self.homepage);
        } else {
            var pageString = "<p>";
            var dates = getFolders("JP-BotTest/", page[0]);
            
            for(var i = 0; i < dates.length; i++)
                pageString += dates[i] + "<br/>";
            
            pageString += "</p>";
            
            self.pageData(pageString);
        }
    }
}

ko.applyBindings(new DiscordViewModel());

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

function getFolders(server, page) {
    var dates = new Array();
    $.ajax({
        async: false,
        url: server + page + "/",
        success: function(data) {
            $(data).find("a").attr("href", function (i, val) {
                if(i > 4) {
                    dates.push(val);
                }
            });
        }
    });
    return dates;
}
