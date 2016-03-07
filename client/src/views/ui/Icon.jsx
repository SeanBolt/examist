import React, { PropTypes } from "react";
import { Link } from "react-router";

export default function Icon(props) {
    let className = `fa fa-${props.name}`;

    if(props.size) className += ` fa-${props.size}x`;
    if(props.active) className += " active";
    if(props.className) className += " " + props.className;

    return (
        <i {...props} className={className} />
    );
}

Icon.propTypes = {
    name: PropTypes.string.isRequired,
    size: PropTypes.number
};

export function IconLink(props) {
    return (<Link to={props.to}><Icon {...props} /></Link>);
}