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

export default function Contact({ application, onClose, updateApplications, email }) {
	const [form] = Form.useForm();

	const closeForm = () => {
		form.resetFields();
		onClose();
	};

	const updateApplication = (values) => {
		const loading = message.loading('Saving...', 0);
		axios
			.post('/api/add_contact_details', {
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
            title="Track Company Communications"
            open={true}
            onCancel={closeForm}
            width={700}
            centered
            footer={[
                <Button type="primary" onClick={() => form.submit()} id="save" key="save">
                    Log New Communication Information
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
                    contactName: application.contact,
                }}
                onFinish={updateApplication}
            >
                <Form.Item label="Contact Information" name="contactName">
                    <Input.TextArea placeholder="Enter Contact Information (name, email, purpose)" />
                </Form.Item>
                <Form.Item
                    label="Set Reminder To Follow Up With Someone"
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
            </Form>
        </Modal>
    );
}
