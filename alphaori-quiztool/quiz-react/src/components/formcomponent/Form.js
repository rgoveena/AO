import React from 'react'
import Styles from './Styles'
import { Form, Field } from 'react-final-form'
import arrayMutators from 'final-form-arrays'
import { FieldArray } from 'react-final-form-arrays'

const sleep = ms => new Promise(resolve => setTimeout(resolve, ms))

const onSubmit = async values => {
    await sleep(300)
    
    const data = new FormData();
    data.append('quiz', JSON.stringify(values));

    fetch('http://localhost:3001/quizzes', {
      method: 'POST',
      body: data
    }).then((res) => giveAlert(res.status));
}

const giveAlert = (statusCode) => {
  if (statusCode===200 || statusCode === 304) {
    alert("Quiz successfully submitted!");
  } else if (statusCode===500){
    alert("Failed to upload quiz, likely due to an already existing quiz with the same name. Please try editing the existing quiz instead, or submit one with a different name.")
  } else {
    alert("Server not responding!")
  }
}

const MyForm = () => (
  <Styles>
    <br/><br/>
    <Form
      onSubmit={onSubmit}
      mutators={{
        ...arrayMutators
      }}
      
      render={({
        handleSubmit,
        form: {
          mutators: { push, pop }
        }, // injected from final-form-arrays above
        pristine,
        form,
        submitting,
        values
      }) => {
        return (
          <form onSubmit={handleSubmit}>
            <div className="md">
              <label>Quiz Name</label>
              <Field name="quizName" component="input" />
              <div className="buttons">
                <button
                  type="button"
                  onClick={() => push('questions', undefined)}>
                  Add Question
                </button>
              </div>
            </div>
            <FieldArray name="questions">
              {({ fields }) =>
                fields.map((name, i) => (
                <div>
                  <div key={name}>
                  <br/>
                    <Field
                      name={`${name}.question`}
                      component="input"
                      placeholder="Question"
                      style={{ width: "350px" }}/>
                    <span
                      onClick={() => fields.remove(i)}
                      style={{ cursor: 'pointer' }}>
                      ❌
                    </span>
                    <div className="buttons" >
                      <button
                        type="button"
                        onClick={() => push(`${name}.answers`, undefined)}
                        style={{ margin: 0 }}>
                        Add Answer 
                      </button>
                    </div>
                  </div>
                  <div>
                      <br/>
                      <FieldArray name={`${name}.answers`}>
                        {({ fields }) =>
                          fields.map((name2, i) => (
                            <div key={name2}>
                              <label>Answer {i + 1}</label>
                              <Field
                                name={`${name2}.content`}
                                component="input"
                                placeholder="Answer"/>
                              <Field
                                name={`${name2}.correct`}
                                component="input"
                                placeholder="Correct (true/false)"/>
                              <span
                                onClick={() => fields.remove(i)}
                                style={{ cursor: 'pointer' }}>
                                ❌
                              </span>
                            </div>
                          ))
                        }
                      </FieldArray>
                  </div>
                </div>
                ))
              }
            </FieldArray>
            
            <div className="buttons">
              <button type="submit" disabled={submitting || pristine}>
                Submit
              </button>
              <button
                type="button"
                onClick={form.reset}
                disabled={submitting || pristine}>
                Reset
              </button>
            </div>
            <pre>{JSON.stringify(values, 0, 2)}</pre>
          </form>
        )
      }}/>
  </Styles>
)

export default MyForm;