import React, { Component } from 'react';
import PropTypes from 'prop-types';

import { withStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import Typography from '@material-ui/core/Typography';

import ws_client from './WebSocketClient.js';

const styles = theme => ({
  card: {
    alignItems: 'center',
  },
  details: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  },
  content: {
    flex: '1 0 auto',
    alignItems: 'center',
  },
});


class CurrentlyPlaying extends Component {
    
    constructor(props){
        super(props);
        this.props = props;

        this.tickerTapeTimer = null;
        this.tickerTapeCounter = 0;

        this.state = {
            currentlyPlaying: null,
            
        };

        ws_client.subscribe("set.current_song", (data)=>{
            this.setState({
                currentlyPlaying: data.payload.song
            });

            if(this.tickerTapeTimer !== null){
                this.tickerTapeCounter = 0;
            }
        });

        ws_client.subscribe("get.current_song", (data)=>{
            this.setState({
                currentlyPlaying: data.payload
            });

            if(this.tickerTapeTimer === null && this.state.currentlyPlaying !== null){
                this.tickerTapeTimer = setInterval(this.ticker_tape, 250)
            }
            else{
                this.state.tickerTapeCounter = 0;
            }
        });

        ws_client.subscribe("set.skip", () => {
            this.setState({
                currentlyPlaying: null
            });
            clearTimeout(this.tickerTapeTimer);
            this.tickerTapeTimer = null;
            this.tickerTapeCounter = 0;
        });

       ws_client.registerInitHook(()=>{
            ws_client.send({type:"command", key:"get.current_song"});
        });
    }


    ticker_tape = () => {
        if (this.tickerTapeCounter >= this.state.currentlyPlaying.title.length){
            this.tickerTapeCounter = -5;
        }

        if(this.tickerTapeCounter < 0){
            document.title = "Doc: " + this.state.currentlyPlaying.title;
            this.tickerTapeCounter += 1
            return
        }

        document.title = "Doc: " + this.state.currentlyPlaying.title.substring(this.tickerTapeCounter, this.state.currentlyPlaying.title.length);

        this.tickerTapeCounter += 1
    }

    render(){
        const { classes, theme } = this.props;
        return (
           <Card className={classes.card}>
               <div className={classes.details}>
                    <CardContent className={classes.content}>
                        <Typography variant="headline" component="h2">
                          Currently Playing
                        </Typography>
                        { this.state.currentlyPlaying === null && <div>
                            <Typography component="h2">
                                <em>Nothing is currently playing</em>
                            </Typography>
                        </div>}
                        { this.state.currentlyPlaying !== null && <div>
                            <Typography component="h2">
                                { this.state.currentlyPlaying !== null && this.state.currentlyPlaying.title}
                            </Typography>
                            <img src={this.state.currentlyPlaying !== null && this.state.currentlyPlaying.thumbnail.url} />
                        </div>}
                        
                    </CardContent>
                </div>
            </Card>
        )
    }
}

CurrentlyPlaying.propTypes = {
  classes: PropTypes.object.isRequired,
  theme: PropTypes.object.isRequired,
};

export default withStyles(styles)(CurrentlyPlaying);
