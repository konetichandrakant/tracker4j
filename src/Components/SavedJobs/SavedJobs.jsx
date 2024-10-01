import React, { useEffect, useState } from 'react';
import { Button, DatePicker, Card, Typography, Select } from 'antd';
import { PlusOutlined } from '@ant-design/icons';
import axios from 'axios';
import { useLocation } from 'react-router-dom';

import AddSavedJob from './AddSavedJob';
import './SavedJobs.scss';
import AddCareerFair from './AddCareerFair';

const sortingOptions = [
	{
	value: 'companyName_Asc',
	label: 'Company Name Asc',
	},
	{
	value: 'companyName_Desc',
	label: 'Company Name Desc',
	}
]

export default function SavedJobs() {
	const [applications, setApplications] = useState([]);
    const [careerfairs, setCareerfairs] = useState([]);
	const [addApplicationOpen, setAddApplicationOpen] = useState(false);
    const [addCareerFairOpen, setAddCareerFairOpen] = useState(false);
	const [loading, setLoading] = useState(true);
	const { state } = useLocation();

	useEffect(() => {
		updateApplications();
        updateCareerFairs();
	}, []);

	const toggleAddApplication = () => setAddApplicationOpen(!addApplicationOpen);
    const toggleAddCareerFair = () => setAddCareerFairOpen(!addCareerFairOpen);

	const updateApplications = (sort="name", asc=true) => {
		axios
			.get('/api/view_applications?email=' + state.email + '&sort=' + sort + "&asc=" + asc)
			.then(({ data }) =>
				setApplications(data.applications.filter((app) => app.status == 'saved'))
			)
			.catch((err) => console.log(err))
			.finally(() => setLoading(false));
	};

	const updateCareerFairs = (sort="url", asc=true) => {
		axios
			.get('/api/view_careerfairs?email=' + state.email + '&sort=' + sort + "&asc=" + asc)
			.then(({ data }) =>
				setCareerfairs(data.applications)
			)
			.catch((err) => console.log(err))
			.finally(() => setLoading(false));
	};


	const handleChange = (value) => {
		var sort = value.split("_")
		updateApplications(sort[0], sort[1] == "Asc")
        updateCareerFairs();
	};

	return (
		<div className="SavedJobs">
			<div className="SubHeader">
				<div className="flex" />
				<Select
					defaultValue="Company Name Asc"
					style={{ width: 220 }}
					onChange={handleChange}
					options={sortingOptions}
					className="sortingDropdown"
					/>
				<Button
					id="add-application"
					type="primary"
					size="large"
					icon={<PlusOutlined />}
					onClick={toggleAddApplication}
				>
					Add Application
				</Button>
                &nbsp;&nbsp;&nbsp;&nbsp;
                <Button
					id="add-career-fair"
					type="primary"
					size="large"
					icon={<PlusOutlined />}
					onClick={toggleAddCareerFair}
				>
					Add Career Fair
				</Button>
				<AddSavedJob
					isOpen={addApplicationOpen}
					onClose={toggleAddApplication}
					updateApplications={updateApplications}
				/>
                <AddCareerFair
					isOpen={addCareerFairOpen}
					onClose={toggleAddCareerFair}
					updateApplications={updateCareerFairs}
				/>
			</div>
            <h1> Saved Jobs </h1>
			<div className="Jobs">
				{loading && (
					<>
						<Card loading />
						<Card loading />
					</>
				)}
				{applications.map((application) => (
					<Card className="Job" key={application._id} title={application.companyName}>
						ID: {application.jobId}
						<br />
						Title: {application.jobTitle}
						<br />
						{'URL: '}
						<a href={'//' + application.url} target={'_blank'}>
							Click here for more details on {application.jobTitle} at {application.companyName}
						</a>
					</Card>
				))}
				{applications.length === 0 && <Typography.Text>No Saved Jobs</Typography.Text>}
			</div>
            <br></br>
            <br></br>
            <br></br><h1> Saved Career Fairs </h1>
            <div className="CareerFairs">
				{loading && (
					<>
						<Card loading />
						<Card loading />
					</>
				)}
				{careerfairs.map((careerfair) => (
					<Card className="Job" key={careerfair._id} title={careerfair.careerFairName}>
						Career Fair Name: {careerfair.careerFairName}
						<br />
						Date: {careerfair.date}
						<br />
						{'URL: '}
						<a href={'//' + careerfair.url} target={'_blank'}>
							Click here for more details on {careerfair.careerFairName}
						</a>
					</Card>
				))}
				{careerfairs.length === 0 && <Typography.Text>No Saved Jobs</Typography.Text>}
			</div>

		</div>
	);
}
