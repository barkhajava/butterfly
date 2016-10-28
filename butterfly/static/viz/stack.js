//-----------------------------------
//
// DOJO.Stack: Stack some tileSources
// New DOJO.Source
//     DOJO.Source.init
// -- Made by main.js
// -- Init by main.js
//-----------------------------------
log = console.log.bind(window.console);

DOJO.Stack = function(src_terms){

    // Setup
    var channels = src_terms.channel || ['i'];
    channels = channels.split('').concat('dojo');
    this.preset = channels.map(this.layerer);
    this.nLayers = this.preset.length;
    // Prepare the sources
    this.protoSource = new DOJO.Source(src_terms);
    this.source = this.make(this.now, new Array(this.nLayers));
    this.index = this.indexer(this.preset);
    this.total = this.source.length;
}

DOJO.Stack.prototype = {
    now: 0,
    level: 0,
    zBuff: {
      start: 0,
      end: 0
    },
    maxBuff: 3,
    layerer: function(char,i){
        var layers = {
            i: {gl:0, mod:''},
            s: {gl:0, mod:'&segmentation=y&segcolor=y'},
            g: {gl:1, target: true, mod:'&segmentation=y'},
            y: {gl:1, target: true, mod:'&synapse=y'},
            dojo: {gl:0, dojo:true}
        };
        var src = layers[char] || layers.i;
        var alpha = 1-Number(src.gl || src.dojo == true);
        var set = {
            opacity: 1-(i>0)*alpha*(0.5)
        }
        return {src:src, set:set}
    },
    make: function(zLevel, indices) {
        return this.preset.map(this.sourcer.bind(this,zLevel,indices));
    },
    share: DOJO.Source.prototype.share.bind(null),
    sourcer: function(zLevel, indices, layer, i){
        var src = {z:zLevel,minLevel:this.level};
        var source = this.protoSource.init(this.share(layer.src, src));
        return this.share(this.share(layer.set, {index:indices[i]}), source);
    },
    indexer: function(preset){
        var buffer = function(zb){
          return preset.map(function(p,i){
              return Math.max(zb,0)*preset.length+i;
          });
        }
        return {
          'start': buffer(0),
          'up': buffer(this.zBuff.start),
          'down': buffer(this.zBuff.start-1),
          'end': buffer(this.zBuff.start+this.zBuff.end-1),
          'now': buffer(this.zBuff.start+this.zBuff.end)
        }
    },
    init: function(osd){
        var w = osd.world;
        this.getItems = function(event){
            return this.index[event].map(w.getItemAt, w);
        }
        this.event = function(event){
            var point = (event=='up')?'end':'start';
            var needed = this.total - w.getItemCount();
            if (needed == 0) {
              return this.getItems(event);
            }
        }
        this.lose = function(lost){
            lost.map(w.getItemAt,w).map(w.removeItem,w);
        }
        this.gain = function(offset, index){
            this.make(offset+this.now, index).map(osd.addTiledImage,osd);
        }
        this.show = function(shown){
            shown.map(w.getItemAt,w).map(function(shownItem){
                w.setItemIndex(shownItem, w.getItemCount()-1);
            });
            this.index.end.map(w.getItemAt,w).map(function(lastItem,i){
                w.setItemIndex(lastItem, shown[i]);
            });
        }
        this.log = function(){
            for(var c = 0; c < w.getItemCount(); c++){
               log(w.getItemAt(c).source.z);
            }
            log(' ');
        }
        this.vp = osd.viewport;
        this.w = w;
        return this;
    },
    updater: function(point,sign){
        if (this.zBuff[point] < this.maxBuff){
            this.zBuff[point] += 1;
            this.total += this.nLayers;
            this.index = this.indexer(this.preset);
            this.gain(sign*this.zBuff[point], this.index[point]);
        }
    },
    refresher: function(e){
        e.item.addHandler('fully-loaded-change',function(e){
            var event = e.eventSource;
            var source = event.source;
            if(e.fullyLoaded){
                if(!this.w.needsDraw()){
                    this.updater('start',-1);
                    this.updater('end',1);
                };
                source.minLevel = 0;
                event.draw();
                return;
            }
        }.bind(this));
    },
    zoomer: function(e){
        var z = Math.max(e.zoom,1);
        var maxLevel = this.source[0].tileSource.maxLevel;
        this.level = Math.min(Math.ceil(Math.log(z)/Math.LN2), maxLevel);
    }
};