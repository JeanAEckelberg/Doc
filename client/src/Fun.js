import React, { Component } from 'react';
import PropTypes from 'prop-types';

// Material referances
import { withStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import Avatar from '@material-ui/core/Avatar';
import Chip from '@material-ui/core/Chip';
import MusicNote from '@material-ui/icons/MusicNote';

import ws_client from './WebSocketClient.js';
import Egg from './egg.js';
import themeManager from './ThemeManager.js';

const styles = theme => ({
  chip: {
    margin: theme.spacing.unit,
  },
});


class Fun extends Component {

    constructor(props){
        super(props);
        this.props = props;

        this.state = {
            limitOn: true
        }

        var egg = new Egg(atob("dXAsdXAsZG93bixkb3duLGxlZnQscmlnaHQsbGVmdCxyaWdodCxiLGE="), function() {
            ws_client.send({
                type: "command",
                key: "toggle.duration_limit"
            }, true);
        }).listen();

        new Egg(atob("bGVmdCxvLHg="), ()=>{
            setInterval(this.obnoxious, 500)
        }).listen();

        new Egg(atob("bGVmdCxz"), ()=>{
            alert("It's party time")
            document.body.classList.add("shake");
        }).listen();

        var egg = new Egg(atob("bGVmdCxjLGwsZSxhLHIscQ=="), function() {
            ws_client.send({
                type: "command",
                key: "remove.queue"
            }, true);
        }).listen();



        ws_client.subscribe("toggle.duration_limit", ()=>{
            this.setState({
                limitOn: !this.state.limitOn
            });
        })

        ws_client.subscribe("get.duration_limit", data=>{
            this.setState({
                limitOn: data.payload.duration_limit
            });
        });


       ws_client.registerInitHook(()=>{
            ws_client.send({type:"command", key:"get.duration_limit"});
        });
    }

    obnoxious(){
        var theme = {
            palette: {
                primary: { main: '#' + Math.random().toString(16).slice(2, 8).toUpperCase() }, 
              secondary: { main: '#' + Math.random().toString(16).slice(2, 8).toUpperCase() }, 
              type: themeManager.rawTheme.palette.type,
            },
        }
        themeManager.updateTheme(theme, false)
    }

    render(){
        var { classes, visibility} = this.props
        visibility = visibility || "visible";
        return (
            <div className={classes.control} style={{"visibility": visibility }}>
            <Chip
                style={{"visibility": !this.state.limitOn ? "visible": "hidden" }}
                avatar={
                    <Avatar>
                        <MusicNote />
                    </Avatar>
                }
                label="Music Overwhelming"
                className={classes.chip}
            />
            </div>
        )
    }

}

export default withStyles(styles)(Fun);
