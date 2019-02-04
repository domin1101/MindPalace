import React from 'react';
import * as d3 from "d3";
import {Command} from "./App";

class FileUpload extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            uploading: false
        };
        this.upload = this.upload.bind(this);
        this.paste = this.paste.bind(this);
    }

    upload(e) {
        const files = Array.from(e.target.files);

        this.props.onSendCommand(Command.UPDATE_FILE, {file: files[0], node_id: this.props.node_id}, () => this.setState({uploading: false}));
    }

    paste() {

    }

    render() {
        let content;

        if (this.state.uploading) {
            content = <i className="fas fa-spinner"></i>
        } else {
            content = <input type='file' id='single' onChange={this.upload} />;
        }

        return (
             <div>
                 {content}
             </div>
        );
    }
}

export default FileUpload;