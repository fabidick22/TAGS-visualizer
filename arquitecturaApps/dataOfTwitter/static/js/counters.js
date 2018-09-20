var __extends = (this && this.__extends) || (function () {
    var extendStatics = Object.setPrototypeOf ||
        ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
        function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
function getRGB(hex) {
    var hexNum = hex.replace('#', '');
    var hexValues = hexNum.match(/.{1,2}/g);
    for (var i = 0; i < hexValues.length; i++) {
        hexValues[i] = parseInt('0x' + hexValues[i], 16);
    }
    return hexValues;
}
function greatDiff(start, end) {
    var stColor = getRGB(start), enColor = getRGB(end), diff = 0;
    for (var i = 0; i < stColor.length; i++) {
        var calcDiff = Math.abs(stColor[i] - enColor[i]);
        if (calcDiff > diff) {
            diff = calcDiff;
        }
    }
    return diff;
}
function convertColor(start, end, step) {
    var startRGB = getRGB(start), endRGB = getRGB(end), result = "#";
    for (var i = 0; i < startRGB.length; i++) {
        var stNum = startRGB[i], enNum = endRGB[i];
        if (stNum != enNum) {
            if (stNum < enNum) {
                startRGB[i]++;
            }
            else if (stNum > enNum) {
                startRGB[i]--;
            }
        }
        var intVer = parseInt(startRGB[i], 10);
        if (intVer < 10) {
            result += '0' + intVer.toString(16);
        }
        else {
            result += (intVer.toString(16).length < 2 ? '0' + intVer.toString(16) : intVer.toString(16));
        }
    }
    return result;
}
var Counter = /** @class */ (function () {
    function Counter(timer) {
        this.timer = timer;
        this.started = false;
        this.numStart = typeof this.timer.data('start') != 'undefined' ? this.timer.data('start') : 0;
        this.numEnd = this.timer.data('finnish');
        this.prepend = typeof this.timer.data('prepend') != 'undefined' ? this.timer.data('prepend') : '';
        this.append = typeof this.timer.data('append') != 'undefined' ? this.timer.data('append') : '';
        this.animateNum = typeof this.timer.data('countanim') != 'undefined' ? this.timer.data('countanim') : true;
        this.count = this.numStart;
        this.speed = typeof this.timer.data('speed') != 'undefined' ? this.timer.data('speed') : 100;
        this.increment = typeof this.timer.data('increment') != 'undefined' ? this.timer.data('increment') : 0;
        // Event listeners for queing on Scroll
        // var _this = this;
        // $(window).on('load scroll', function() {
        // 	var scrollPos = $(this).scrollTop(),
        // 		midView = $(this).height() / 1.5 + scrollPos,
        // 		counterPos = _this.timer.offset().top;
        // 	if(midView >= counterPos && _this.started == false) {
        // 		_this.displayLoop();
        // 	}
        // });
        this.displayLoop();
    }
    Counter.prototype.displayLoop = function () {
        var _this = this;
        this.started = true;
        if (this.animateNum == true) {
            this.timer.find('.display').html("<span class=\"decorator prepend\">" + this.prepend + "</span><span class=\"count\">" + this.count + "</span><span class=\"decorator append\">" + this.append + "</span>");
        }
        if (this.count < this.numEnd) {
            this.loop = setTimeout(function () {
                _this.displayLoop();
            }, this.speed);
            if (this.increment > 0 && this.numEnd - this.count > this.increment) {
                this.count += this.increment;
            }
            else {
                this.count++;
            }
        }
    };
    Counter.prototype.prependCanvas = function (canvas) {
        this.timer.prepend(canvas);
    };
    Counter.prototype.getTimer = function () {
        return this.timer;
    };
    Counter.prototype.getCount = function () {
        return this.count;
    };
    Counter.prototype.getTotal = function () {
        return this.numEnd;
    };
    Counter.prototype.getStarted = function () {
        return this.started;
    };
    return Counter;
}());
var Radial = /** @class */ (function (_super) {
    __extends(Radial, _super);
    function Radial(timer) {
        var _this = _super.call(this, timer) || this;
        var _timer = _super.prototype.getTimer.call(_this);
        _this.cClockwise = typeof _timer.data('cclockwise') != 'undefined' ? _this.timer.data('cclockwise') : false;
        var canvas = $('<canvas/>', { "class": 'progress-bar' }).attr({ 'width': 350, 'height': 240 });
        _super.prototype.prependCanvas.call(_this, canvas);
        // Radial bar
        _this.radialBar = _timer.find('.progress-bar')[0];
        _this.radialColor = typeof _timer.data('color') != 'undefined' ? _this.timer.data('color') : '#000';
        _this.startColor = _this.radialColor;
        _this.endColor = typeof _timer.data('endcolor') != 'undefined' ? _this.timer.data('endcolor') : _this.radialColor;
        _this.xPos = _this.radialBar.width / 2;
        _this.yPos = _this.radialBar.height / 2 + 10;
        _this.radialProgress = _this.radialBar.getContext('2d');
        _this.setStage();
        _this.displayLoop();
        return _this;
    }
    Radial.prototype.setStage = function () {
        var radius = 95;
        var startAngle = .75 * Math.PI;
        var endAngle = 2.25 * Math.PI;
        var counterClock = false;
        // Set position and width
        this.radialProgress.beginPath();
        this.radialProgress.arc(this.xPos, this.yPos, radius, startAngle, endAngle, counterClock);
        this.radialProgress.lineWidth = 60;
        // line color
        this.radialProgress.strokeStyle = '#444';
        // this.radialProgress.lineCap = 'butt';
        this.radialProgress.stroke();
    };
    Radial.prototype.drawProgress = function (percent) {
        var radius = 95;
        if (this.cClockwise) {
            var startAngle = 2.25 * Math.PI;
            var position = (percent * (.75 - 2.25) / 100) + 2.25;
            var endAngle = (position >= .75 ? position : .75) * Math.PI;
        }
        else {
            var startAngle = .75 * Math.PI;
            var position = (percent * (2.25 - .75) / 100) + .75;
            var endAngle = (position <= 2.25 ? position : 2.25) * Math.PI;
        }
        this.radialProgress.beginPath();
        this.radialProgress.arc(this.xPos, this.yPos, radius, startAngle, endAngle, this.cClockwise);
        this.radialProgress.lineWidth = 40;
        // this.radialProgress.lineCap = 'round';
        // line color
        if (this.radialColor == this.endColor) {
            this.radialProgress.strokeStyle = this.radialColor;
        }
        else {
            this.startColor = convertColor(this.startColor, this.endColor, percent);
            this.radialProgress.strokeStyle = this.startColor;
        }
        this.radialProgress.stroke();
    };
    Radial.prototype.displayLoop = function () {
        var _started = _super.prototype.getStarted.call(this);
        _super.prototype.displayLoop.call(this);
        var _count = _super.prototype.getCount.call(this);
        if (typeof this.radialProgress != "undefined") {
            this.radialProgress.clearRect(0, 0, this.radialBar.width, this.radialBar.height);
            this.setStage();
            this.drawProgress(_count);
        }
    };
    return Radial;
}(Counter));
var Grid = /** @class */ (function (_super) {
    __extends(Grid, _super);
    function Grid(timer) {
        var _this = _super.call(this, timer) || this;
        var _timer = _super.prototype.getTimer.call(_this);
        _this.dotGrid = _timer.find('.grid');
        for (var i = 0; i < 100; ++i) {
            _this.dotGrid.append($('<span/>'));
        }
        _this.dots = _this.dotGrid.find('span');
        _this.displayLoop();
        return _this;
    }
    Grid.prototype.gridProgress = function (position) {
        $(this.dots).eq(0).addClass('active');
        $(this.dots).eq(position - 1).addClass('active');
    };
    Grid.prototype.displayLoop = function () {
        _super.prototype.displayLoop.call(this);
        var _count = _super.prototype.getCount.call(this);
        this.gridProgress(_count);
    };
    return Grid;
}(Counter));
var counters = [];
$('.js-counter').each(function (i) {
    counters[i] = new Counter($(this));
});
var radials = [];
$('.js-radial').each(function (i) {
    radials[i] = new Radial($(this));
});
var grids = [];
$('.js-grid').each(function (i) {
    grids[i] = new Grid($(this));
});