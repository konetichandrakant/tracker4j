/* eslint-disable react/prop-types */
import React, { useEffect, useState } from 'react';
import { Button, DatePicker, Form, Input, message, Modal, Select } from 'antd';
import moment from 'moment';
import axios from 'axios';

export default function ChooseAction({ application, onClose, email }) {
    const [form] = Form.useForm();

    const closeForm = () => {
		onClose();
	};

	return (
        <div>
            <div>
                <Modal
                    title="What change occured within this job search?"
                    open={true}
                    onCancel={closeForm}
                    width={700}
                    centered
                    footer={[
                        <Button id="moving_on" type="primary" size="small" onClick= {() => setContacts(application)}>
                            Someone reached out.
                        </Button>,
                        <Button id="moving_on" type="primary" size="small" onClick= {() => setNextStageApplication(true)}>
                            I've moved on. Log next steps.
                        </Button>,
                        <Button id="rejected" type="primary" size="small" onClick= {() => rejected(application)}>
                            I've been rejected.
                        </Button>
                    ]}
                >
                    <div>
                        Job Title : {application.jobTitle}
                        <br />
                        Notes : {application.description}
                    </div>
                </Modal>
            </div>
        </div>

	);
}
