define('yadage', ["jupyter-js-widgets","vis"], function(widgets,vis) {

    var WorkflowWidgetView = widgets.DOMWidgetView.extend({

        render: function() {
            this.value_changed();
            this.model.on('change:dotstring', this.value_changed, this);
        },


        value_changed: function() {
            var data = this.model.get('dotstring');
            this.el.innerHTML = ''
            this.container = document.createElement('div');
            this.container.innerHTML = 'hello'
            this.el.appendChild(this.container);
            this.container.style.height="200px";
            this.container.style.width="200px";
            var DOTstring = data;
            console.log('hello')
            console.log(DOTstring)
            console.log('done')
            console.log(data)
            console.log('done2')
            var parsedData = vis.network.convertDot(DOTstring);
            this.netdata = {
              nodes: parsedData.nodes,
              edges: parsedData.edges
            }
            this.net_options = parsedData.options;
            this.net_options.layout = {
                hierarchical: {
                    direction: 'UD',
                    sortMethod: 'directed'
                }
            }
            this.network = new vis.Network(this.container, this.netdata, this.net_options);
            console.log(this.netdata.nodes)
        },
    });
    return {
        WorkflowWidgetView : WorkflowWidgetView
    };
});
