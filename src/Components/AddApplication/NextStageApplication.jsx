/* eslint-disable react/prop-types */
import React from 'react';
import { Button, DatePicker, Form, Input, message, Modal, Select } from 'antd';
import moment from 'moment';
import axios from 'axios';

const statuses = {
	interview: 'Interview',
	rejected: 'Rejected',
	accepted: 'Accepted',
};

export default function NextStageApplication({ application, onClose, updateApplications, email }) {
	const [form] = Form.useForm();

	const closeForm = () => {
		form.resetFields();
		onClose();
	};

	const updateApplication = (values) => {
		const loading = message.loading('Saving...', 0);
		axios
			.post('/api/next_stage_application', {
				...values,
				_id: application._id,
				email,
			})
			.then(({ data }) => {
				message.success(data.message);
				updateApplications();
			})
			.catch((err) => message.error(err.response.data?.error))
			.finally(() => {
				loading();
				closeForm();
			});
	};

	return (
		<Modal
			title="Change in Application Status - Update Stage"
			open={true}
			onCancel={closeForm}
			width={700}
			centered
			footer={[
				<Button type="primary" onClick={() => form.submit()} id="save" key="save">
					Update Application
				</Button>,
			]}
		>
			<div>
				Company Name : {application.companyName}
				<br />
				Job Title : {application.jobTitle}
				<hr />
            </div>
			<Form
				form={form}
				layout="vertical"
				requiredMark={false}
				initialValues={{
					description: application.description,
					status: 'interview'
				}}
				onFinish={updateApplication}
			>
				<Form.Item label="Notes" name="description">
					<Input.TextArea placeholder="Enter Notes" />
				</Form.Item>
				<Form.Item
					label="We have your back! Set a reminder and we will send you an email alert!"
					name="reminder"
					rules={[
						{
							required: true,
							message: 'Enter Date that You Need to Take Your Next Action Before!',
						},
					]}
				>
					<DatePicker />
				</Form.Item>
                <Form.Item
					label="Set Interview Date"
					name="interview"
					rules={[
						{
							required: true,
							message: 'Set your interview date!',
						},
					]}
				>
					<DatePicker />
				</Form.Item>
				<Form.Item
					label="Status"
					name="status"
					rules={[
						{
							required: true,
							message: 'Please enter your new Status!',
						},
					]}
				>
					<Select>
						{Object.keys(statuses).map((key) => (
							<Select.Option value={key} key={key}>
								{statuses[key]}
							</Select.Option>
						))}
					</Select>
				</Form.Item>
			</Form>
		</Modal>
	);
}
