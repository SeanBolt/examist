import React, { Component, PropTypes } from "react";
import { Flex } from "../ui/layout";

export default class PDFView extends Component {
    static propTypes = {
        link: PropTypes.string.isRequired
    };

    render() {
        return (
            <Flex className="PDFView">
                <object data={this.props.link} type="application/pdf"/>
            </Flex>
        );
    }
}