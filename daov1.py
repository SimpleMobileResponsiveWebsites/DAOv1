import streamlit as st
import pandas as pd
from datetime import datetime

# Simulate a simple token distribution and DAO system
class DAO:
    def __init__(self):
        self.members = {"alice": 100, "bob": 200, "carol": 50}  # Members with tokens
        self.proposals = []
        self.treasury_balance = 1000  # Initial treasury balance in DAO

    def add_proposal(self, title, description):
        proposal = {
            "id": len(self.proposals) + 1,
            "title": title,
            "description": description,
            "votes": {"yes": 0, "no": 0},
            "created_at": datetime.now(),
            "status": "Pending"
        }
        self.proposals.append(proposal)

    def vote(self, proposal_id, vote):
        if vote not in ["yes", "no"]:
            raise ValueError("Vote must be 'yes' or 'no'")
        
        # Find the proposal and cast vote
        proposal = next(p for p in self.proposals if p["id"] == proposal_id)
        
        if vote == "yes":
            proposal["votes"]["yes"] += 1
        elif vote == "no":
            proposal["votes"]["no"] += 1

    def update_proposals_status(self):
        for proposal in self.proposals:
            if proposal["votes"]["yes"] > proposal["votes"]["no"]:
                proposal["status"] = "Accepted"
            else:
                proposal["status"] = "Rejected"
                
    def get_proposals(self):
        return pd.DataFrame(self.proposals)

# Initialize DAO
dao = DAO()

# Streamlit App Interface
st.title("Decentralized Autonomous Organization (DAO) Simulation")

# Display current treasury balance
st.sidebar.header("DAO Treasury")
st.sidebar.write(f"Current Treasury Balance: ${dao.treasury_balance}")

# Add a proposal
st.header("Add New Proposal")
proposal_title = st.text_input("Proposal Title")
proposal_description = st.text_area("Proposal Description")

if st.button("Submit Proposal"):
    if proposal_title and proposal_description:
        dao.add_proposal(proposal_title, proposal_description)
        st.success(f"Proposal '{proposal_title}' submitted successfully!")

# Voting section
st.header("Vote on Proposals")
dao.update_proposals_status()  # Update proposal statuses before voting

# Display existing proposals and voting options
proposals_df = dao.get_proposals()
if not proposals_df.empty:
    for _, proposal in proposals_df.iterrows():
        st.subheader(proposal["title"])
        st.write(f"Description: {proposal['description']}")
        st.write(f"Status: {proposal['status']}")
        st.write(f"Votes: Yes - {proposal['votes']['yes']}, No - {proposal['votes']['no']}")

        # Voting options
        vote_choice = st.radio(f"Cast your vote on {proposal['title']}", ["Yes", "No"], key=proposal["id"])
        if st.button(f"Vote on {proposal['title']}", key=f"vote_{proposal['id']}"):
            dao.vote(proposal["id"], vote_choice.lower())
            st.success(f"Your vote on '{proposal['title']}' has been cast as '{vote_choice}'")

else:
    st.write("No proposals available to vote on currently.")

# Display all proposals
if st.button("Show all proposals"):
    st.write(proposals_df)

