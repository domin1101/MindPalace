import React from 'react';
import * as d3 from "d3";
import EditNode from "./EditNode";

class EditBar extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            focusedNode: "00000000-0000-0000-0000-000000000000",
            nodeListing: []
        };
    }

    componentDidMount() {
    }

    addNodesRecursive(nodeListing, node, level, maxLevels) {
        nodeListing.push({node: node, level: level});

        if (level < maxLevels) {
            for (const child of node.children) {
                this.addNodesRecursive(nodeListing, child, level + 1, maxLevels);
            }
        }
    }

    componentDidUpdate(prevProps, prevState) {
        if (prevProps.nodes !== this.props.nodes && this.state.focusedNode in this.props.nodes) {
            var nodeListing = [];
            const focusedNode = this.props.nodes[this.state.focusedNode];
            this.addNodesRecursive(nodeListing, focusedNode, 0, 2);

            this.setState({
                nodeListing: nodeListing
            });
        }
    }

    render() {
        return (
             <div>
                 {this.state.nodeListing.map((element) => (
                     <EditNode
                         key={element.node.id}
                         node={element.node}
                         level={element.level}
                         onSendCommand={this.props.onSendCommand}
                        />
                 ))}
             </div>
        );
    }
}

export default EditBar;