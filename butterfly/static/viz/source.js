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
    source.mod += ['','&output=zip'][source.gl];
    return {tileSource: source};
  },
  tileSource: {
    z: 0,
    mod: '',
    server: '',
    datapath: '',
    minLevel: 0,
    width: 8192,
    height: 8192,
    tileSize: 512,
    getTileUrl: function( level, x, y ) {

      if (this.dojo) {
        return '/images/pix.png?'+[level,x,y].join('-');
      }
      var blevel = this.maxLevel - level;
      var width = this.getTileWidth(level);
      var height = this.getTileHeight(level);
      var bounds = this.getTileBounds(level, x, y).getSize();
      var shape = bounds.times(this.getLevelScale(level)*this.width);
      var size = [Math.round(shape.x), Math.round(shape.y), 1];
      var start = [x*width, y*height, this.z];

      return this.server + '/data/?datapath=' + this.datapath + '&start=' +
        start + '&mip=' + blevel + '&size=' +  size + this.mod;
    }
  },
  share: function(from, to) {
    for (var key in from) {
      to[key] = from[key];
    }
    return to;
  }
}
