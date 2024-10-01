import React, { useEffect, useState } from 'react';
import { Button, DatePicker, Form, Input, message, Skeleton, Typography } from 'antd';
import { useLocation } from 'react-router-dom';
import Plot from 'react-plotlyjs';
import axios from 'axios';

import './Statistics.scss';

export default function Statistics() {
    const [plot, setPlot] = useState(0);
    const [indicators, setIndicators] = useState(0);
	const [loading, setloading] = useState(true);
	const { state } = useLocation();

	useEffect(() => {
		axios
			.get('/api/get_statistics?email=' + state.email)
			.then(data=> {
                setPlot(data.data);
			})
			.catch((err) => message.error(err.response?.data?.error))
			.finally(() => setloading(false));
        axios
			.get('/api/get_statistics_indicators?email=' + state.email)
			.then(data=> {
                setIndicators(data.data);
			})
			.catch((err) => message.error(err.response?.data?.error))
			.finally(() => setloading(false));
	}, []);


	return (
        <div>
            <div className="statistics_page" style={{ display: 'flex', justifyContent: 'center'}}>
                <Plot data={indicators.data} layout={indicators.layout}/>
            </div>
            <div className="statistics_page" style={{ display: 'flex', justifyContent: 'center'}}>
                <Plot data={plot.data} layout={plot.layout}/>
            </div>
        </div>
	);
	}