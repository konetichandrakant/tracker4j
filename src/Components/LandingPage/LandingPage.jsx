import React, { useEffect, useState } from 'react';
import { Button, Card, Tag, Typography, Dropdown, Select, Input, Modal } from 'antd';
import { EditFilled, PlusOutlined, ArrowRightOutlined } from '@ant-design/icons';
import axios from 'axios';
import { useLocation } from 'react-router-dom';

import AddApplication from '../AddApplication/AddApplication';
import EditApplication from '../AddApplication/EditApplication';
import NextStageApplication from '../AddApplication/NextStageApplication';
import Contact from '../AddApplication/Contact';
import ChooseAction from '../AddApplication/ChooseAction';
import ChangeOutcome from '../AddApplication/ChangeOutcome';
import './LandingPage.scss';


// const clmns = {
// applied, int, deci
// };
const columns = {
	applied: 'Applied',
	interview: 'Interview',
	decision: 'Decision',
};

const sortingOptions = [
	{
	value: 'companyName_Asc',
	label: 'Company Name Asc',
	},
	{
	value: 'companyName_Desc',
	label: 'Company Name Desc',
	},
	{
	value: 'date_Asc',
	label: 'Date Asc',
	},
	{
	value: 'date_Desc',
	label: 'Date Desc',
	}
]

export default function LandingPage() {
	const [applications, setApplications] = useState([]);
	const [page, setPage] = useState(1);
	const [prev, setPrev] = useState(false);
	const [next, setNext] = useState(false);
	const [filter, setFilter] = useState("");
	const [sort, setSort] = useState("name_Asc");
	const [loading, setLoading] = useState(true);
	const [addApplicationOpen, setAddApplicationOpen] = useState(false);
	const [editApplication, setEditApplication] = useState(false);
	const [nextStageApplication, setNextStageApplication] = useState(false);
	const [contacted, setContacts] = useState(false);
	const [chooseAction, setNextAction] = useState(false);
	const [changeOutcome, setOutcome] = useState(false);
	const { state } = useLocation();
	const [interviewModel, setInterviewModel] = useState(false)
	const [upcomingInterviews, setUpcomingInterviews] = useState([])

	useEffect(() => {
		updateApplications();
		fetchUpcomingInterviews();
	}, [sort, filter, page]);
	
	const fetchUpcomingInterviews = () => {
		axios.get('/api/interviews?email=' + state.email).then(({ data }) => {
			console.log(data)
			setUpcomingInterviews(data)
		})
	}

	const updateApplications = () => {
		axios
			.get('/api/view_applications?email=' + state.email + '&sort=' + sort.split("_")[0] + "&asc=" + (sort.split("_")[1] == "Asc") + "&filter=" + filter + "&page=" + page)
			.then(({ data }) => {
				setApplications(data.applications)
				if (!data.applications) setNext(true)
				else setNext(false)
				if (page == 1) setPrev(true)
				else setPrev(false)
			})
			.catch((err) => console.log(err))
			.finally(() => setLoading(false));
	};

	const handleChange = (value) => {
		setSort(value)
		updateApplications()
	};

	const toggleAddApplication = () => setAddApplicationOpen(!addApplicationOpen);

	const onSearch = (string) => {
		setFilter(string)
	};

	const handlePrev = () => {
		setPage(page-1)
	}

	const handleNext = () => {
		setPage(page+1)
	}

	const closeUpcomingInterviewModal = () => {
		setInterviewModel(false)
	}

	const openUpcomingInterviewModal = () => {
		setInterviewModel(true)
	}

	return (
		<div className="LandingPage">
			<div className="SubHeader">
				<Input.Search
					placeholder="search text"
					allowClear
					enterButton="Search"
					size="large"
      				style={{ width: 400 }}
      				onSearch={onSearch}
				id="search-bar"
				/>
				<Button onClick={openUpcomingInterviewModal} id="upcoming-interviews">Upcoming interviews</Button>
				<div className="flex" />
				
				<Select
					defaultValue="Company Name Asc"
					style={{ width: 220 }}
					onChange={handleChange}
					options={sortingOptions}
					className="sortingDropdown"
					id="sort-button"
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
				<AddApplication
					isOpen={addApplicationOpen}
					onClose={toggleAddApplication}
					updateApplications={updateApplications}
				/>
			</div>

			<div className="MainContent">
				{Object.keys(columns).map((col) => (
					<div className="Status" key={col}>
						<Typography.Title level={5}>{columns[col]}</Typography.Title>
						{loading ? (
							<>
								<Card loading bordered={false} />
								<Card loading bordered={false} />
								<Card loading bordered={false} />
							</>
						) : (
							applications.map(
								(application, index) =>
									(application.status === col ||
										(col === 'decision' &&
											['rejected', 'accepted'].includes(
												application.status
											))) && (
										<Card
											key={col + index}
											title={application.companyName}
											extra={
												<><Button
													type="text"
													icon={<EditFilled />}
													onClick={() => setEditApplication(application)}
													id={application.jobId + 'edit'} />
														
													</>
											}
											className="Job"
											bordered={false}
											actions={
												[
												application.status === 'accepted' ? (
													<Tag color="#87d068">Accepted</Tag>
												) : (
													application.status === 'rejected' && (
														<Tag color="#f50">Rejected</Tag>
													)
												),
												application.status === 'applied' ? (
													<div><Tag color="#FFB6C1" onClick={() => setContacts(application)}>Log Contact</Tag>
														<Tag color="#FFA500" onClick={() => setNextStageApplication(application)}>Got the Interview?</Tag>
													</div>
												) : null,
												application.status === 'interview' ? (
													<div><Tag color="#FFB6C1" onClick={() => setContacts(application)}>Log Contact</Tag>
														<Tag color="#A020F0" onClick={() => setOutcome(application)}>Change Outcome</Tag>
													</div>
												) : null,
												]
											}
										>
											ID: {application.jobId}
											<br />
											Title: {application.jobTitle}
											<br />
											<a href={'//' + application.url} target={'_blank'}>
												{'URL to Job Posting'}
											</a>
											<br />
											Notes: {application.description}
											<br />
											Upcoming Interview: {application.interview}
											<br />
											Action Needed By: {application.reminder}
										</Card>
									)
							)
						)}
						{applications.length === 0 && 'No applications found.'}
					</div>
				))}
			</div>
			<div>
				<Button onClick={handlePrev} disabled={prev}>Prev</Button>
				<span>{page}</span>
				<Button onClick={handleNext} disabled={next}>Next</Button>
			</div>
			{editApplication && (
				<EditApplication
					application={editApplication}
					onClose={() => setEditApplication(false)}
					updateApplications={updateApplications}
					email={state.email}
				/>
			)}
			{nextStageApplication && (
				<NextStageApplication
					application={nextStageApplication}
					onClose={() => setNextStageApplication(false)}
					updateApplications={updateApplications}
					email={state.email}
				/>
			)}
			{contacted && (
				<Contact
					application={contacted}
					onClose={() => setContacts(false)}
					updateApplications = {updateApplications}
					email={state.email}
				/>
			)}
			{chooseAction && (
				<ChooseAction
					application={chooseAction}
					onClose={() => setNextAction(false)}
					email={state.email}
				/>
			)}
			{changeOutcome && (
				<ChangeOutcome
					application={changeOutcome}
					onClose={() => setOutcome(false)}
					updateApplications={updateApplications}
					email={state.email}
				/>
			)}
			{interviewModel && (
				<Modal open={true} title="Upcoming interviews" onOk={closeUpcomingInterviewModal} onCancel={closeUpcomingInterviewModal} onClose={closeUpcomingInterviewModal}>
					{upcomingInterviews.map(({ companyName, date, jobTitle }, index) => {
						return (
							<div key={index}>
								<div> Company: {companyName}</div>
								<div>Date: {date.slice(0,11)}</div>
								<div>Job: {jobTitle}</div>
								<hr/>
							</div>

						)
					}) }
				</Modal>
			)}
		</div>
	);
}
