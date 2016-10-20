//-----------------------------------
//
// DOJO.Source: makes tileSources
// -- Made & Init by DOJO.Stack
//-----------------------------------

DOJO.Source = function(src_terms){
    // Change the default source terms
    this.tileSource = this.share(src_terms, this.tileSource);
}

DOJO.Source.prototype = {
    init: function(src_terms){
        var sourcer = this.share(this.tileSource,{});
        var source = this.share(src_terms, sourcer);
        var maxLevel = source.width/source.tileSize;
        source.maxLevel = Math.floor(Math.log2(maxLevel));
        // Get the segmentation string for butterfly
        if (source.segmentation) {
            source.seg = '&segmentation=y&'+this.segmentFormats[source.gl];
        }
        return {tileSource: source};
    },
    segmentFormats: ['segcolor=y','output=zip'],
    tileSource: {
        z: 0,
        seg: '',
        minLevel: 0,
        width: 8192,
        height: 8192,
        tileSize: 512,
        server: window.location.href.split('/')[2],
        datapath: '/Volumes/NeuroData/cylindojo/mojo',
        getTileUrl: function( level, x, y ) {
            var rats = this.getPixelRatio(level);
            var bounds = this.getTileBounds(level, x, y).getSize();
            var size = Object.keys(rats).map(function(xy){
                return bounds[xy]/rats[xy];
            });
            size.push(1);
            var blevel = this.maxLevel - level;
            var width = this.getTileWidth(level);
            var height = this.getTileHeight(level);
            var start = [x*width, y*height, this.z];
              return 'http://' + this.server + '/data/?datapath=' + this.datapath +
                '&start=' + start + '&mip=' + blevel + '&size=' +  size + this.seg;
        }
    },
    share: function(from, to) {
        for (var key in from) {
           to[key] = from[key];
        }
        return to;
    }
};