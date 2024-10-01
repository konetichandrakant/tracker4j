/* eslint-disable react/prop-types */
import React from 'react';
import { Button, DatePicker, Form, Input, message, Modal, Select } from 'antd';
import moment from 'moment';
import axios from 'axios';

const statuses = {
	applied: 'Applied',
	interview: 'Interview',
	rejected: 'Rejected',
	accepted: 'Accepted',
};

export default function ChangeOutcome({ application, onClose, updateApplications, email }) {
	const [form] = Form.useForm();

	const closeForm = () => {
		form.resetFields();
		onClose();
	};

	const updateApplication = (values) => {
		const loading = message.loading('Saving...', 0);
		axios
			.post('/api/change_status', {
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
		<div>
		<Modal
			title="Change Outcome of Application"
			open={true}
			onCancel={closeForm}
			width={700}
			centered
            footer={[
				<Button type="primary" onClick={() => form.submit()} id="save" key="save">
					Change Outcome
				</Button>,
			]}
		>
			<Form
				form={form}
				layout="vertical"
				requiredMark={false}
				initialValues={{
					status: application.status
				}}
				onFinish={updateApplication}
			>
			
				<Form.Item
					label="Status"
					name="status"
					rules={[
						{
							required: true,
							message: 'Please enter Status!',
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
		</div>
	);
}
